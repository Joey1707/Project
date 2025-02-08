import { NavLink, useRouteError } from "react-router";

export default function ErrorPage() {
	const error = useRouteError();
	console.error(`${error.status || "404"}: ${error.message || error || "Error message not found"}`);

	return (
		<div className="h-full lg:w-[40%] md:w-[60%] w-[80%] md:max-h-full max-h-[80%] flex flex-col md:gap-4 gap-2 p-6 bg-white justify-between items-center rounded-md">
			<h1 className="font-bold md:text-4xl text-2xl">
				Error Code: {error.status || "404"}
			</h1>
      <div className="h-full flex flex-col justify-between m-3 border-y-2 gap-4 md:p-6 p-2">
        <h2 className="font-bold md:text-3xl text-xl">Error Message:</h2>
        <p className="md:text-xl text-lg text-gray-600 p-4 bg-gray-200 rounded-md h-full">
          {error.message || error || "Error message not found"}
        </p>
      </div>
			<NavLink
				to="/"
				className="md:text-4xl text-2xl font-bold underline text-blue-700"
			>
				Back to Home Page
			</NavLink>
		</div>
	);
}
