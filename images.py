# from  PIL import Image
# import base64
# import io
# from typing import Optional
# from fastapi import Depends, APIRouter, HTTPException, Response,UploadFile,File
# from models import Image
# import models
# from database import engine, SessionLocal
# from sqlalchemy.orm import Session
# from fastapi.responses import HTMLResponse,StreamingResponse
# from typing import List




# router=APIRouter(
#     prefix="/images",
#     tags=["IMAGES"],
#     responses={404:{"description":"not found"}}
# )
# models.Base.metadata.create_all(bind=engine)
# def get_db():
#     try: 
#         db=SessionLocal()
#         yield db
#     finally:
#         db.close()


# # Endpoint to upload a file
# @router.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     # Read the file content and save to the database
#     image_data = Image(data=file.file.read())
#     db.add(image_data)
#     db.commit()
#     db.refresh(image_data)
#     return {"filename": file.filename}

# @router.get("/images/")
# async def get_images(db: Session = Depends(get_db)):
#     images = db.query(Image).all()
#     image_data_list = []
#     for image in images:
#         image_data = io.BytesIO(base64.b64decode(image.data))
#         img = Image.open(image_data)
#         img.show()
#         buffered = io.BytesIO()
#         img.save(buffered, format="JPEG")
#         image_data_list.append(buffered.getvalue())
#     return StreamingResponse(io.BytesIO(image_data_list[0]), media_type="image/jpeg")



# @router.get("/images/")
# async def get_images(db: Session = Depends(get_db)):
#     images = db.query(Image).all()
#     return [{"id": image.id, "data": base64.b64encode(image.data).decode()} 












# @router.post("/uploadimage/")
# async def create_upload_image(file: UploadFile = File(...)):
#     # Read image content and save to database
#     db = SessionLocal()
#     try:
#         img = Image.open(io.BytesIO(await file.read()))
#         img_data = img.tobytes()
#         # Stream the image data to the database to avoid loading it all into memory
#         image_data = ImageData(data=img_data)
#         db.add(image_data)
#         db.commit()
#         db.refresh(image_data)
#         return {"filename": file.filename}
#     finally:
#         db.close()

# @router.get("/{image_id}")
# async def get_image(image_id: int, db: Session = Depends(get_db)):
#     # Retrieve image data from the database
#     image_data = db.query(ImageData).filter(ImageData.id == image_id).first()
#     if not image_data:
#         raise HTTPException(status_code=404, detail="Image not found")

#     try:
#         # Convert binary data to an image using PIL library
#         img = Image.open(io.BytesIO(image_data.data)) 
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error opening image: {e}")

#     try:
#         # Return the image as a response
#         img = Image.open(io.BytesIO(image_data.data))
#         img_io = io.BytesIO()
#         img.save(img_io, format="".format)
#         img_io.seek(0)
#         return Response(content=img_io.getvalue(), media_type=f"image/{img.format}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error returning image: {e}")




























