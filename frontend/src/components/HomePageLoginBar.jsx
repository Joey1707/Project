import { useEffect, useState } from "react";
import { NavLink } from "react-router";
import { buttonHover } from "../styles/reusableSyles";
import { verifyToken } from "../utils/network_data";

export default function HomePageLoginBar() {
  const [isLoading, setIsLoading] = useState(true)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const isVerified = await verifyToken();
        setIsLoggedIn(isVerified); // Update state
      } catch(err) {
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    };

    checkLoginStatus();
  }, []);

  if (isLoading) { // While API is verifying token return a loading message
    return <h1 className="font-bold text-xl text-gray-600 text-center">Checking login status, please wait...</h1>
  } else if (isLoggedIn) { //If API returns user is logged in then creates a clickable nav link to the dashboard
    return (
      <h1 className="text-center font-bold md:text-2xl text-lg">
        Anda sudah login, silahkan ke{" "}
        <NavLink
          className="font-bold md:text-2xl text-lg text-blue-500 underline"
          to="/dashboard"
        >
          dashboard
        </NavLink>
      </h1>
    )
  } else { //If API returns user is not logged in then offers the user to login or create an account
    return (
      <div className="flex md:flex-row flex-col justify-between md:p-4 md:gap-12 gap-4">
      <NavLink
        to="/login"
        className={
          "font-bold md:text-xl text-lg text-center border-2 p-2 rounded-md w-full cursor-pointer" +
          buttonHover
        }
      >
        Masuk Akun
      </NavLink>
      <NavLink
        to="/register"
        className={
          "font-bold md:text-xl text-lg text-center border-2 p-2 rounded-md w-full cursor-pointer" +
          buttonHover
        }
      >
        Buat Akun
      </NavLink>
    </div>
    )
  }
}