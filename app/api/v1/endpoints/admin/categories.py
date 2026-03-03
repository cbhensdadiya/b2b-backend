from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.deps import require_permission
from app.models import User, Category, Subcategory, AuditLog
from pydantic import BaseModel, Field
from datetime import datetime
import math

router = APIRouter()


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    icon: Optional[str] = None
    image_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    show_on_home: bool = True
    show_in_menu: bool = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    slug: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    icon: Optional[str] = None
    image_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    show_on_home: Optional[bool] = None
    show_in_menu: Optional[bool] = None


class SubcategoryCreate(BaseModel):
    category_id: str
    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    icon: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


@router.get("/categories")
def list_categories(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_permission("categories.view")),
    db: Session = Depends(get_db)
):
    """
    List all categories with filtering and pagination
    - Requires: categories.view permission
    """
    query = db.query(Category).filter(Category.deleted_at == None)
    
    if is_active is not None:
        query = query.filter(Category.is_active == is_active)
    
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))
    
    query = query.order_by(Category.display_order, Category.name)
    
    total = query.count()
    total_pages = math.ceil(total / page_size)
    
    categories = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "data": [cat.to_dict() for cat in categories],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.post("/categories")
def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(require_permission("categories.create")),
    db: Session = Depends(get_db)
):
    """
    Create a new category
    - Requires: categories.create permission
    """
    # Check if slug already exists
    existing = db.query(Category).filter(Category.slug == category_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category slug already exists")
    
    category = Category(
        **category_data.dict(),
        created_by=current_user.id
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE",
        entity_type="Category",
        entity_id=category.id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Category created successfully", "data": category.to_dict()}


@router.put("/categories/{category_id}")
def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    current_user: User = Depends(require_permission("categories.edit")),
    db: Session = Depends(get_db)
):
    """
    Update a category
    - Requires: categories.edit permission
    """
    category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update fields
    update_data = category_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    category.updated_by = current_user.id
    category.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(category)
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE",
        entity_type="Category",
        entity_id=category_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Category updated successfully", "data": category.to_dict()}


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: str,
    current_user: User = Depends(require_permission("categories.delete")),
    db: Session = Depends(get_db)
):
    """
    Soft delete a category
    - Requires: categories.delete permission
    """
    category = db.query(Category).filter(Category.id == category_id, Category.deleted_at == None).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.deleted_at = datetime.utcnow()
    category.deleted_by = current_user.id
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="DELETE",
        entity_type="Category",
        entity_id=category_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Category deleted successfully"}


@router.get("/subcategories")
def list_subcategories(
    category_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(require_permission("subcategories.view")),
    db: Session = Depends(get_db)
):
    """
    List all subcategories
    - Requires: subcategories.view permission
    """
    query = db.query(Subcategory).filter(Subcategory.deleted_at == None)
    
    if category_id:
        query = query.filter(Subcategory.category_id == category_id)
    
    query = query.order_by(Subcategory.display_order, Subcategory.name)
    
    total = query.count()
    total_pages = math.ceil(total / page_size)
    
    subcategories = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "data": [sub.to_dict() for sub in subcategories],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.post("/subcategories")
def create_subcategory(
    subcategory_data: SubcategoryCreate,
    current_user: User = Depends(require_permission("subcategories.create")),
    db: Session = Depends(get_db)
):
    """
    Create a new subcategory
    - Requires: subcategories.create permission
    """
    # Verify category exists
    category = db.query(Category).filter(Category.id == subcategory_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    subcategory = Subcategory(
        **subcategory_data.dict(),
        created_by=current_user.id
    )
    
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE",
        entity_type="Subcategory",
        entity_id=subcategory.id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Subcategory created successfully", "data": subcategory.to_dict()}


class SubcategoryUpdate(BaseModel):
    category_id: Optional[str] = None
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    slug: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


@router.put("/subcategories/{subcategory_id}")
def update_subcategory(
    subcategory_id: str,
    subcategory_data: SubcategoryUpdate,
    current_user: User = Depends(require_permission("subcategories.edit")),
    db: Session = Depends(get_db)
):
    """
    Update a subcategory
    - Requires: subcategories.edit permission
    """
    subcategory = db.query(Subcategory).filter(
        Subcategory.id == subcategory_id,
        Subcategory.deleted_at == None
    ).first()
    
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    
    # If category_id is being updated, verify new category exists
    if subcategory_data.category_id:
        category = db.query(Category).filter(Category.id == subcategory_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Update fields
    update_data = subcategory_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subcategory, key, value)
    
    subcategory.updated_by = current_user.id
    subcategory.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(subcategory)
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE",
        entity_type="Subcategory",
        entity_id=subcategory_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Subcategory updated successfully", "data": subcategory.to_dict()}


@router.delete("/subcategories/{subcategory_id}")
def delete_subcategory(
    subcategory_id: str,
    current_user: User = Depends(require_permission("subcategories.delete")),
    db: Session = Depends(get_db)
):
    """
    Soft delete a subcategory
    - Requires: subcategories.delete permission
    """
    subcategory = db.query(Subcategory).filter(
        Subcategory.id == subcategory_id,
        Subcategory.deleted_at == None
    ).first()
    
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    
    subcategory.deleted_at = datetime.utcnow()
    subcategory.deleted_by = current_user.id
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="DELETE",
        entity_type="Subcategory",
        entity_id=subcategory_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "Subcategory deleted successfully"}



from fastapi import UploadFile, File
import pandas as pd
import io


@router.post("/categories/upload-excel")
async def upload_categories_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(require_permission("categories.create")),
    db: Session = Depends(get_db)
):
    """
    Upload categories from Excel file
    - Requires: categories.create permission
    - Accepts: .xlsx, .xls, .csv files
    - Returns: Summary of created, updated, and failed records
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload .xlsx, .xls, or .csv file"
        )
    
    try:
        # Read file content
        contents = await file.read()
        
        # Parse Excel/CSV file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        # Validate required columns
        required_columns = ['name', 'slug']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process records
        created = 0
        updated = 0
        failed = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Check if category exists by slug
                existing_category = db.query(Category).filter(
                    Category.slug == row['slug'],
                    Category.deleted_at == None
                ).first()
                
                # Prepare category data
                category_data = {
                    'name': row['name'],
                    'slug': row['slug'],
                    'description': row.get('description', None) if pd.notna(row.get('description')) else None,
                    'icon': row.get('icon', None) if pd.notna(row.get('icon')) else None,
                    'image_url': row.get('image_url', None) if pd.notna(row.get('image_url')) else None,
                    'display_order': int(row.get('display_order', 0)) if pd.notna(row.get('display_order')) else 0,
                    'is_active': str(row.get('is_active', 'true')).lower() == 'true' if pd.notna(row.get('is_active')) else True,
                    'show_on_home': str(row.get('show_on_home', 'true')).lower() == 'true' if pd.notna(row.get('show_on_home')) else True,
                    'show_in_menu': str(row.get('show_in_menu', 'true')).lower() == 'true' if pd.notna(row.get('show_in_menu')) else True
                }
                
                if existing_category:
                    # Update existing category
                    for key, value in category_data.items():
                        setattr(existing_category, key, value)
                    existing_category.updated_by = current_user.id
                    existing_category.updated_at = datetime.utcnow()
                    updated += 1
                    
                    # Log action
                    audit = AuditLog(
                        user_id=current_user.id,
                        action="UPDATE",
                        entity_type="Category",
                        entity_id=str(existing_category.id)
                    )
                    db.add(audit)
                else:
                    # Create new category
                    new_category = Category(**category_data)
                    new_category.created_by = current_user.id
                    db.add(new_category)
                    created += 1
                    
                    # Flush to get the ID
                    db.flush()
                    
                    # Log action
                    audit = AuditLog(
                        user_id=current_user.id,
                        action="CREATE",
                        entity_type="Category",
                        entity_id=str(new_category.id)
                    )
                    db.add(audit)
                
            except Exception as e:
                failed += 1
                errors.append(f"Row {index + 2}: {str(e)}")
                continue
        
        # Commit all changes
        db.commit()
        
        return {
            "success": True,
            "message": "File processed successfully",
            "created": created,
            "updated": updated,
            "failed": failed,
            "errors": errors[:10]  # Limit to first 10 errors
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/subcategories/upload-excel")
async def upload_subcategories_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(require_permission("subcategories.create")),
    db: Session = Depends(get_db)
):
    """
    Upload subcategories from Excel file
    - Requires: subcategories.create permission
    - Accepts: .xlsx, .xls, .csv files
    - Supports mapping by category_name OR category_id
    - Returns: Summary of created, updated, and failed records
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload .xlsx, .xls, or .csv file"
        )
    
    try:
        # Read file content
        contents = await file.read()
        
        # Parse Excel/CSV file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        # Validate required columns - need either category_name or category_id
        required_columns = ['name', 'slug']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Check if we have at least one category mapping column
        if 'category_name' not in df.columns and 'category_id' not in df.columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide either 'category_name' or 'category_id' column"
            )
        
        # Process records
        created = 0
        updated = 0
        failed = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                category_id = None
                
                # Try to get category_id first (if provided)
                if 'category_id' in df.columns and pd.notna(row.get('category_id')):
                    category_id = row['category_id']
                
                # If no category_id, try to find by category_name
                elif 'category_name' in df.columns and pd.notna(row.get('category_name')):
                    category_name = str(row['category_name']).strip()
                    category = db.query(Category).filter(
                        Category.name == category_name,
                        Category.is_active == True,
                        Category.deleted_at == None
                    ).first()
                    
                    if category:
                        category_id = str(category.id)
                    else:
                        failed += 1
                        errors.append(f"Row {index + 2}: Category '{category_name}' not found")
                        continue
                else:
                    failed += 1
                    errors.append(f"Row {index + 2}: No category_name or category_id provided")
                    continue
                
                # Verify category exists
                category = db.query(Category).filter(
                    Category.id == category_id,
                    Category.deleted_at == None
                ).first()
                
                if not category:
                    failed += 1
                    errors.append(f"Row {index + 2}: Category ID {category_id} not found")
                    continue
                
                # Check if subcategory exists by slug and category
                existing_subcategory = db.query(Subcategory).filter(
                    Subcategory.category_id == category_id,
                    Subcategory.slug == row['slug'],
                    Subcategory.deleted_at == None
                ).first()
                
                # Prepare subcategory data
                subcategory_data = {
                    'category_id': category_id,
                    'name': row['name'],
                    'slug': row['slug'],
                    'description': row.get('description', None) if pd.notna(row.get('description')) else None,
                    'icon': row.get('icon', None) if pd.notna(row.get('icon')) else None,
                    'display_order': int(row.get('display_order', 0)) if pd.notna(row.get('display_order')) else 0,
                    'is_active': str(row.get('is_active', 'true')).lower() == 'true' if pd.notna(row.get('is_active')) else True
                }
                
                if existing_subcategory:
                    # Update existing subcategory
                    for key, value in subcategory_data.items():
                        setattr(existing_subcategory, key, value)
                    existing_subcategory.updated_by = current_user.id
                    existing_subcategory.updated_at = datetime.utcnow()
                    updated += 1
                    
                    # Log action
                    audit = AuditLog(
                        user_id=current_user.id,
                        action="UPDATE",
                        entity_type="Subcategory",
                        entity_id=str(existing_subcategory.id)
                    )
                    db.add(audit)
                else:
                    # Create new subcategory
                    new_subcategory = Subcategory(**subcategory_data)
                    new_subcategory.created_by = current_user.id
                    db.add(new_subcategory)
                    created += 1
                    
                    # Flush to get the ID
                    db.flush()
                    
                    # Log action
                    audit = AuditLog(
                        user_id=current_user.id,
                        action="CREATE",
                        entity_type="Subcategory",
                        entity_id=str(new_subcategory.id)
                    )
                    db.add(audit)
                
            except Exception as e:
                failed += 1
                errors.append(f"Row {index + 2}: {str(e)}")
                continue
        
        # Commit all changes
        db.commit()
        
        return {
            "success": True,
            "message": "File processed successfully",
            "created": created,
            "updated": updated,
            "failed": failed,
            "errors": errors[:10]  # Limit to first 10 errors
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )
