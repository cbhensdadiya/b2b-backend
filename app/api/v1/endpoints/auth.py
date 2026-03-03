from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.models.user import User, UserRole
from app.schemas.auth import (
    SignupRequest, SignupResponse,
    LoginRequest, LoginResponse,
    OTPVerificationRequest, OTPVerificationResponse,
    ResendOTPRequest, ResendOTPResponse,
    BuyerResponse
)
from app.services.otp_service import OTPService
from app.services.sms_service import SMSService
from app.api.deps import get_current_buyer

router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def buyer_signup(
    signup_data: SignupRequest,
    db: Session = Depends(get_db)
):
    """
    Buyer signup endpoint with Firebase verification
    
    - Creates new buyer account
    - If firebase_uid provided, user is already verified via Firebase
    - If no firebase_uid, generates and sends OTP for mobile verification (legacy)
    - Password is hashed with BCrypt (cost factor 12)
    - Role is automatically set to 'Buyer'
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == signup_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if mobile already exists
    existing_mobile = db.query(User).filter(User.mobile == signup_data.mobile).first()
    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )
    
    # Hash password
    password_hash = get_password_hash(signup_data.password)
    
    # Check if Firebase UID provided (Firebase-verified signup)
    firebase_uid = getattr(signup_data, 'firebase_uid', None)
    is_verified = bool(firebase_uid)  # If Firebase UID exists, user is verified
    
    # Create new buyer
    new_buyer = User(
        name=signup_data.name,
        email=signup_data.email,
        mobile=signup_data.mobile,
        password_hash=password_hash,
        role=UserRole.BUYER,
        is_verified=is_verified,
        firebase_uid=firebase_uid
    )
    
    db.add(new_buyer)
    db.commit()
    db.refresh(new_buyer)
    
    # If Firebase verified, send welcome SMS
    if is_verified:
        SMSService.send_welcome_sms(signup_data.mobile, signup_data.name)
        message = "Signup successful. Account verified."
    else:
        # Legacy flow: Generate and send OTP
        otp_code = OTPService.create_otp(db, signup_data.mobile)
        SMSService.send_otp(signup_data.mobile, otp_code)
        message = "Signup successful. OTP sent to mobile."
    
    return SignupResponse(
        message=message,
        buyer_id=str(new_buyer.id),
        mobile=signup_data.mobile
    )


@router.post("/verify-otp", response_model=OTPVerificationResponse)
def verify_otp(
    otp_data: OTPVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Verify mobile OTP
    
    - Validates OTP code
    - Marks buyer as verified
    - OTP expires after configured time
    """
    # Verify OTP
    is_valid = OTPService.verify_otp(db, otp_data.mobile, otp_data.otp)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Mark user as verified
    user = db.query(User).filter(User.mobile == otp_data.mobile).first()
    if user:
        user.is_verified = True
        db.commit()
        
        # Send welcome SMS
        SMSService.send_welcome_sms(user.mobile, user.name)
    
    return OTPVerificationResponse(
        message="Mobile number verified successfully",
        success=True
    )


@router.post("/resend-otp", response_model=ResendOTPResponse)
def resend_otp(
    resend_data: ResendOTPRequest,
    db: Session = Depends(get_db)
):
    """
    Resend OTP to mobile number
    
    - Invalidates old OTPs
    - Generates new OTP
    - Sends via SMS
    """
    # Check if mobile exists
    user = db.query(User).filter(User.mobile == resend_data.mobile).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mobile number not found"
        )
    
    # Invalidate old OTPs
    OTPService.invalidate_old_otps(db, resend_data.mobile)
    
    # Generate and send new OTP
    otp_code = OTPService.create_otp(db, resend_data.mobile)
    SMSService.send_otp(resend_data.mobile, otp_code)
    
    return ResendOTPResponse(
        message="OTP resent successfully"
    )


@router.post("/login", response_model=LoginResponse)
def buyer_login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Buyer login endpoint
    
    - Authenticates buyer with email and password
    - Returns JWT access token and refresh token
    - Buyer must be verified to login
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is a buyer
    if user.role != UserRole.BUYER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Buyer access only."
        )
    
    # Check if user is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Mobile number not verified. Please verify your mobile number."
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    return LoginResponse(
        token=access_token,
        refresh_token=refresh_token,
        buyer=user.to_dict()
    )


@router.get("/me", response_model=BuyerResponse)
def get_current_buyer_info(
    current_buyer: User = Depends(get_current_buyer),
    db: Session = Depends(get_db)
):
    """
    Get current buyer information
    
    - Requires authentication
    - Returns buyer profile data
    """
    return BuyerResponse(**current_buyer.to_dict())
