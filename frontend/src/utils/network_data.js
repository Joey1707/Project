import axios from "axios";
import { ErrorAlert } from "./alert_templates";

// Write async fetch functions here
const clientId =
	"1016937893935-uha6eu2vjndkm05i4irid40rbvkvnila.apps.googleusercontent.com";
const BASE_PROD_URL = "https://backend-orcin-gamma.vercel.app";
const BASE_DEV_URL = "http://127.0.0.1:5000";

function getAccessToken() {
	return localStorage.getItem("token");
}

function putAccessToken(token) {
	localStorage.setItem("token", token);
}

function validatePassword(password) {
	// Define regex patterns
	const hasSymbol = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
	const hasCapitalLetter = /[A-Z]/;
	const hasNumber = /[0-9]/;

	let errorMessage = "";

	// Check length
	if (password.length < 6 || password.length > 20) {
		errorMessage = `${errorMessage} Password must be between 6 and 20 characters,`;
	}
	// Check for at least 1 symbol
	if (!hasSymbol.test(password)) {
		errorMessage = `${errorMessage} Password must contain at least 1 symbol,`;
	}
	// Check for at least 1 capital letter
	if (!hasCapitalLetter.test(password)) {
		errorMessage = `${errorMessage} Password must contain at least 1 capital letter,`;
	}
	// Check for at least 1 number
	if (!hasNumber.test(password)) {
		errorMessage = `${errorMessage} Password must contain at least 1 number.`;
	}

	if (errorMessage !== "") {
		return { errorMessage, isValid: false };
	}

	// If all checks pass
	console.log("Password is valid.");
	return { errorMessage, isValid: true };
}

function validateEmail(email) {
	const regex =
		/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	if (regex.test(email)) {
		return true;
	} else {
		return false;
	}
}

class errorObject extends Error {
	constructor(status, message) {
		super(message); // Call the parent Error class constructor
		this.status = status; // Add a custom property
	}
}

async function returnCredentials() {
	// Choose the URL based on the environment (production or local)
	const returnCredentialsURL =
		process.env.NODE_ENV === "production"
			? `${BASE_PROD_URL}/dashboard`
			: `${BASE_DEV_URL}/dashboard`;
	const token = localStorage.getItem("token"); // Get token from localStorage

	// Make the POST request to the dashboard route
	const response = await axios.post(
		returnCredentialsURL,
		{},
		{
			headers: {
				Authorization: `Bearer ${token}`,
				"Content-Type": "application/json",
			},
		}
	);

	// If the response is successful, return the user data
	return response.data; // { username, email }
}

async function registerUser(userData) {
	try {
		// Choose the URL based on the environment (production or local)
		const registerURL =
			process.env.NODE_ENV === "production"
				? `${BASE_PROD_URL}/register`
				: `${BASE_DEV_URL}/register`;

		// Make the POST request
		const response = await axios.post(registerURL, userData);
		console.log("Server response:", response.data);
		return { error: false };
	} catch (error) {
		// Handle errors
		ErrorAlert("Register Failed", error.message);
		console.error(
			"Error submitting the form:",
			error.response?.data || error.message
		);
		return { error: true };
	}
}

async function loginUser(userData) {
	try {
		// Select the login URL based on the environment
		const loginURL =
			process.env.NODE_ENV === "production"
				? `${BASE_PROD_URL}/login`
				: `${BASE_DEV_URL}/login`;

		// Make the POST request
		const response = await axios.post(loginURL, userData);

		// Check if the login was successful and handle the token
		if (response.data.token) {
			const token = response.data.token;
			console.log("Login successful, token stored:", token);
			return { error: false, token }; // Returning the token on success
		} else {
			throw errorObject(404, "No token found in the response");
		}
	} catch (error) {
		// Handle any errors
		ErrorAlert("Login Failed", error.message);
		console.error(
			"Error submitting the form:",
			error.response?.data || error.message
		);
		return { error: true, token: null };
	}
}

////////////////////////////////////////////////////////////////////////////

const verifyToken = async () => {
	const token = getAccessToken();

	if (!token) {
		console.log("There is no token");
		return false;
	}

	const verifyTokenURL =
		process.env.NODE_ENV === "production"
			? `${BASE_PROD_URL}/verify-token`
			: `${BASE_DEV_URL}/verify-token`;
	const response = await axios.post(
		verifyTokenURL,
		{},
		{
			headers: {
				Authorization: `Bearer ${token}`,
				"Content-Type": "application/json",
			},
		}
	);

	if (response.status === 200) {
		return true; // Token is valid
	} else {
		return false; // Token is invalid or an error occurred
	}
};

export {
	clientId,
	getAccessToken,
	putAccessToken,
	validateEmail,
	validatePassword,
	registerUser,
	loginUser,
	errorObject,
	verifyToken,
	returnCredentials,
};
