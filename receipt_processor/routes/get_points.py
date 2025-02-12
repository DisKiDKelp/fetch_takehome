from fastapi import APIRouter, HTTPException, Request

from receipt_processor.models import ProcessedReceipt

from .helper import calculate_points

router = APIRouter()


@router.get("/receipts/{receipt_id}/points")
async def get_points(
    request: Request,
    receipt_id: str,
) -> dict:
    """Get points endpoint."""

    if receipt_id not in request.app.state.reciept_ids:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")

    processed_receipt: ProcessedReceipt = request.app.state.reciept_ids[receipt_id]
    points = processed_receipt.points

    if points is not None:
        # Already been calculated
        return {"points": points}

    processed_receipt.points = calculate_points(processed_receipt.receipt)

    # If first time calculating, update both stores for consistency
    request.app.state.reciept_hashs[processed_receipt.hash_value] = processed_receipt
    request.app.state.reciept_ids[processed_receipt.unique_id] = processed_receipt

    return {"points": processed_receipt.points}
