from fastapi import APIRouter, HTTPException, Depends
from app.model.category_model import Category
from app.dependencies import verify_auth0_token

router = APIRouter(
    prefix="/category",
    tags=["category"],
    dependencies=[Depends(verify_auth0_token)]
)

@router.get("/all")
async def get_all_categories():
    try:
        categories = await Category.find_all().to_list()
        return categories
    except Exception as exc:
        print(f"Error in get_all_categories: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
