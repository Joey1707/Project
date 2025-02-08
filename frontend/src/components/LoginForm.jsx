// Hooks
import useInput from "../hooks/useInput";
import useVisibility from "../hooks/useVisibility";
import { useState } from "react";
import { useNavigate } from "react-router";

// Components
import { WarningAlert } from "../utils/alert_templates";
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa";

// Utils
import { buttonHover, inputStyle } from "../styles/reusableSyles";
import { loginUser, putAccessToken } from "../utils/network_data";

export default function LoginForm() {
	const [email, setEmail] = useInput("");
	const [passwd, setPassword] = useInput("");
	const [isVisible, toggleVisible] = useVisibility();
	const [isFetching, setIsFetching] = useState(false);
	const navigate = useNavigate();

	const onSubmitHandler = async (event) => {
		event.preventDefault();
		console.log(`Submitting data: ${email}, ${passwd}`);

		if (!isFetching) {
			setIsFetching(true);
			const { error, token } = await loginUser({ email, passwd });
			if (!error) {
				// If login is successful, store the token and redirect
				setIsFetching(false);
				putAccessToken(token);
				navigate("/dashboard"); // Redirect to the dashboard or any other protected route
			}
			setIsFetching(false);
		} else {
			WarningAlert(
				"Please Wait!",
				"Mohon tunggu sebentar, data anda sedang di cek server!"
			);
		}
	};

	return (
		<form
			onSubmit={onSubmitHandler}
			className="flex flex-col justify-between md:p-4 p-2 w-full h-full gap-4"
		>
			<div className="flex flex-col h-full w-full justify-center md:gap-6 gap-2">
				<label htmlFor="emailLogin" className="font-bold md:text-2xl text-lg">
					Email:
				</label>
				<input
					id="emailLogin"
					type="email"
					value={email}
					placeholder="email"
					onChange={setEmail}
					className={inputStyle}
					required
				/>
				<label htmlFor="passwordLogin" className="font-bold md:text-2xl text-lg">
					Password:{" "}
				</label>
				<div className="relative h-auto">
					<input
						id="passwordLogin"
						type={isVisible ? "text" : "password"}
						value={passwd}
						placeholder="password"
						onChange={setPassword}
						className={inputStyle}
						required
					/>
					<button
						type="button"
						className="absolute right-[2%] md:top-[30%] top-[24%] text-2xl cursor-pointer z-1"
						onClick={toggleVisible}
					>
						{isVisible ? <FaRegEye /> : <FaRegEyeSlash />}
					</button>
				</div>
			</div>
			<button
				type="submit"
				className={
					"font-bold border-4 rounded-md md:mt-10 mt-4 text-xl md:p-4 p-3 cursor-pointer " +
					buttonHover
				}
				disabled={isFetching}
			>
				{isFetching? "Submitting..." : "Submit"}
			</button>
		</form>
	);
}
