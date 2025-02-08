import { NavLink } from "react-router";
import notfound from "../assets/notfound.png";

export default function NotFoundPage() {
	return (
		<section className="w-[80%] h-full flex justify-between items-center p-12 gap-6 shadow-2xl rounded-lg bg-white">
			<img
				src={notfound}
				alt="not_found_page_img"
				className="max-w-xl p-6 drop-shadow-lg"
			/>
			<div className="flex flex-col h-full w-full p-6 justify-between items-center gap-8 max-w-[50%]">
				<h1 className="font-bold text-4xl p-6 w-full text-center">
					404: Page Not Found
				</h1>
				<p className="flex items-center p-6 h-full text-xl text-center text-gray-500  border-y-2 border-dashed">
					Halaman yang anda cari tidak ada atau tidak ditemukan, jika
					anda merasa ini merupakan bug silahkan menghubungi pihak
					developer
				</p>
				<NavLink
					className="font-bold text-2xl p-2 w-full text-center border-4 rounded-md cursor-pointer 
          transition-all delay-50 duration-300 ease-out
          hover:border-4 hover:bg-gray-900 hover:text-white hover:outline-2 hover:outline-gray-600 hover:outline-offset-8 hover:border-gray-500"
					to="/"
				>
					Return to Homepage
				</NavLink>
			</div>
		</section>
	);
}
