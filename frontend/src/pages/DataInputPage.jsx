import { useLoaderData, useNavigate, useNavigation } from "react-router";
import { errorObject, verifyToken } from "../utils/network_data";
import { useEffect } from "react";
import LoadingPage from "./LoadingPage";

export default function DataInputPage() {
  const navigation = useNavigation();
  const isVerified = useLoaderData();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isVerified) {
      navigate("/");
    }
  }, [isVerified, navigate]);

  if (navigation.state === "loading") {
    return <LoadingPage />;
  }

  return (
    <section className="flex flex-row justify-between h-full w-full bg-white rounded-xl shadow-xl p-6 m-3">
      <h1>TODO: Add data input features</h1>
    </section>
  );
}

// Corrected named export for the loader function
export const dataInputLoader = async () => {
  try {
    const isVerified = await verifyToken();
    return isVerified;
  } catch (err) {
    console.error(err);
    throw new errorObject(err.response.status, `${err}, ${err.response.statusText}, ${err.code}`);
  }
};
