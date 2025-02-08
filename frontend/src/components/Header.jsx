import { NavLink } from "react-router";
import Navigation from "./Navigation";

export default function Header() {
	return (
		<header className="flex md:flex-row flex-col justify-between md:px-18 md:py-8 gap-4 items-center shadow-2xl p-6 md:h-auto">
			<NavLink
				to="/"
				className="font-bold lg:text-4xl text-center text-gray-800 items-center border-b-2 sm:text-3xl text-2xl md:w-40"
			>
				AI App
			</NavLink>
			<Navigation />
			<div className="xl:w-[6%] xl:inline hidden"></div>
		</header>
	);
}
