import { Suspense } from "react";
import { classNames } from "@/shared/lib/classNames";
import { Navbar } from "@/widgets/Navbar";
import { AppRouter } from "./providers/router";

function App() {
  return (
    <div className={classNames("app", {}, [])}>
      <Suspense fallback="Loading...">
        <Navbar />
        <div className="content-page">
          <AppRouter />
        </div>
      </Suspense>
    </div>
  );
}

export default App;
