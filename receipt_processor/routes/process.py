import hashlib

from fastapi import APIRouter, Request

from receipt_processor.models import ProcessedReceipt, Receipt

router = APIRouter()


@router.post("/receipts/process")
async def receipts_process(reciept: Receipt, request: Request):
    """Process reciept endpoint."""

    # Use deterministic hash to check for duplicates
    reciept_bytes = bytes(str(reciept.model_dump()).encode("utf-8"))
    hash_value = hashlib.sha256(reciept_bytes).hexdigest()

    # If we've seen the reciept before, just return
    if found_receipt := request.app.state.reciept_hashs.get(hash_value):
        return {"id": found_receipt.unique_id}

    # Otherwise, add it to seen reciepts
    processed_receipt = ProcessedReceipt(hash_value=hash_value, receipt=reciept)

    # Add receipt to hashs for quicker access
    request.app.state.reciept_hashs[hash_value] = processed_receipt
    request.app.state.reciept_ids[processed_receipt.unique_id] = processed_receipt

    return {"id": processed_receipt.unique_id}
