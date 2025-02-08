import { useNavigation } from "react-router";
import HomePageLoginBar from "../components/HomePageLoginBar";
import LoadingPage from "./LoadingPage";

export default function HomePage() {
  const navigation = useNavigation()

  if (navigation.state === "loading") {
    return <LoadingPage/>
  }

  return (
    <section className="flex flex-col justify-between lg:w-[60%] md:w-[80%] md:max-h-full w-full h-[90%] p-6 m-4 shadow-2xl rounded-md bg-white md:gap-4">
      <h1 className="font-bold md:text-4xl text-2xl text-center md:p-4">
        Tentang aplikasi AI kami
      </h1>
      <div className="flex flex-col items-center justify-between h-full w-full md:px-10 md:py-6 p-4 gap-12">
        <p className="md:text-xl border-t-2 md:p-6 p-2 text-lg">
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
          Doloribus nesciunt, praesentium rerum in nostrum corporis et
          asperiores eos culpa aut.
        </p>
        <nav className="w-full p-4 border-t-2">
          <h4 className="md:text-lg text-center underline md:underline-offset-8 md:mb-4 mb-2">
            Mulai menggunakan aplikasi
          </h4>
          <HomePageLoginBar />
        </nav>
      </div>
    </section>
  );
}
