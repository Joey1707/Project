import { NavLink } from "react-router";
import RegisterForm from "../components/RegisterForm";

export default function RegisterPage() {
	return (
		<section className="flex flex-col md:gap-3 gap-1 md:px-12 p-2 items-center justify-between h-full lg:w-[60%] md:w-[70%] w-full shadow-xl bg-white rounded-md">
			<h1 className="font-bold md:text-3xl text-2xl border-b-2 border-dashed p-6 w-full text-center">
				Silahkan buat akun
			</h1>
			<RegisterForm />
			<p className="text-gray-600 font-medium border-t-2 p-6 w-full border-dashed text-center">
				Sudah punya akun?{" "}
				<NavLink to="/login" className="text-blue-600 hover:underline">
					Masuk akun
				</NavLink>
			</p>
		</section>
	);
}
