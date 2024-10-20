from fastapi import APIRouter, Response, status, HTTPException
from src.Books.schemas import Book, Book_Input
from bson import ObjectId

book_router = APIRouter()


@book_router.get("/")
async def get_all_books():
    books = await Book.find().to_list()
    return books


@book_router.get("/{book_id}")
async def get_books_by_id(book_id):
    book = await Book.find_one({"_id": ObjectId(book_id)})
    if book is not None:
        return Response(
            content=book.model_dump_json(),
            status_code=status.HTTP_200_OK,
            media_type="application/json",
        )
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.post("/")
async def post_books(book: Book_Input):

    book_data = Book(title=book.title)
    await book_data.insert()

    return Response(
        content="Book inserted successfully",
        status_code=status.HTTP_201_CREATED,
    )


@book_router.patch("/{book_id}")
async def patch_books(book_id: str, book: Book_Input):
    await Book.find_one({"_id": ObjectId(book_id)}).set({"title": book.title})
    book_data = await Book.find_one({"_id": ObjectId(book_id)})
    return Response(
        content=book_data.model_dump_json(),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )


@book_router.delete("/{book_id}")
async def delete_books(book_id: str):
    result = await Book.find_one({"_id": ObjectId(book_id)}).delete()
    if result.deleted_count == 0:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
