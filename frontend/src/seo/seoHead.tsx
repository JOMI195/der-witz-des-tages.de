import { Outlet } from "react-router-dom";
import useSeo from "./useSeo";

const SeoHead = () => {
  useSeo();
  return <Outlet />;
};

export default SeoHead;
