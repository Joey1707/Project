import {
  errorObject,
  returnCredentials,
  verifyToken,
} from "../utils/network_data";
// Hooks
import { useContext, useEffect } from "react";
import { useLoaderData, useNavigate, useNavigation } from "react-router";

// Components
import DashboardGraph from "../components/DashboardGraph";
import UserProfile from "../components/UserProfile";
import LoadingPage from "./LoadingPage";

// Context
import UserContext from "../contexts/UserContext";

export default function DashboardPage() {
  const navigation = useNavigation();
  const { isVerified, profileInfo } = useLoaderData();
  const { userInfo, setUserInfo } = useContext(UserContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isVerified) {
      navigate("/");
    }
    setUserInfo(profileInfo);
    // Log updated state only when it changes
    console.log("User info updated:", profileInfo);
  }, [isVerified, profileInfo, navigate, setUserInfo]);

  if (navigation.state === "loading") {
    return <LoadingPage />;
  }

  return (
    <section className="w-full h-full flex flex-row justify-between p-6 gap-4">
      <UserProfile />
      <DashboardGraph />
    </section>
  );
}

// Named export for the loader function
export const dashboardLoader = async () => {
  try {
    const isVerified = await verifyToken();
    const profileInfo = await returnCredentials();
    return { isVerified, profileInfo };
  } catch (err) {
    console.error(err);
    throw new errorObject(err.response?.status, `${err}, ${err.response?.statusText}, ${err.code}`);
  }
};
