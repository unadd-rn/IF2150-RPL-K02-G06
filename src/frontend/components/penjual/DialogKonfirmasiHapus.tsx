"use client";

interface DialogKonfirmasiHapusProps {
    isOpen: boolean;
    namaMakanan: string;
    isDeleting: boolean;
    onConfirm: () => void;
    onCancel: () => void;
    }

    export default function DialogKonfirmasiHapus({
    isOpen,
    namaMakanan,
    isDeleting,
    onConfirm,
    onCancel,
    }: DialogKonfirmasiHapusProps) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
            <h3 className="text-lg font-bold text-gray-900">Confirm Listing Deletion</h3>
            <p className="mt-2 text-sm text-gray-600">
            Are you sure you want to delete the food listing{" "}
            <span className="font-semibold text-gray-900">&ldquo;{namaMakanan}&rdquo;</span>? This will remove the listing from the customer catalog.
            </p>

            <div className="mt-6 flex justify-end gap-3">
            <button
                type="button"
                onClick={onCancel}
                disabled={isDeleting}
                className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
            >
                Cancel
            </button>
            <button
                type="button"
                onClick={onConfirm}
                disabled={isDeleting}
                className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50"
            >
                {isDeleting ? "Deleting..." : "Yes, Delete"}
            </button>
            </div>
        </div>
        </div>
    );
}
