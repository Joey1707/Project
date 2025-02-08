import Swal from "sweetalert2";

function ErrorAlert(title, errorMessage) {
	Swal.fire({
		title: title,
		text: errorMessage,
		icon: "error",
		confirmButtonText: "Continue",
	});
}

function WarningAlert(title, warningMessage) {
  Swal.fire({
		title: title,
		text: warningMessage,
		icon: "warning",
		confirmButtonText: "Continue",
	});
}

export { ErrorAlert, WarningAlert };
