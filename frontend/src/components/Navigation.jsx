import { NavLink } from "react-router";
import { buttonHover } from "../styles/reusableSyles";

export default function Navigation() {
	return (
		<nav className="flex lg:w-[80%] items-center justify-center h-10 w-full">
			<ul className="flex flex-row items-center justify-center w-full divide-gray-700 divide-x-3">
				<li className="flex items-center justify-center md:p-1 xl:w-[20%] w-full">
					<NavLink
						to="/dashboard"
						className={
							"md:text-2xl text-xl text-center text-gray-800 font-bold m-1 p-1 border-b-2 rounded-sm " +
							buttonHover
						}
					>
						Dashboard
					</NavLink>
				</li>
				<li className="flex items-center justify-center p-1 xl:w-[20%] h-[70%] w-full">
					<NavLink
						to="/input"
						className={
							"md:text-2xl text-xl text-center text-gray-800 font-bold m-1 p-1 border-b-2 rounded-sm " +
							buttonHover
						}
					>
						Input Data
					</NavLink>
				</li>
			</ul>
		</nav>
	);
}
