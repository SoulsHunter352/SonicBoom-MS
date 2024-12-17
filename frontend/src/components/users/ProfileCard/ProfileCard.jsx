import UserAvatar from "../UserAvatar/UserAvatar";
import classes from "./ProfileCard.module.css";
import FormButton from "../../Form/FormButton/FormButton";
import { Link } from "react-router-dom";

export default function ProfileCard({ children }) {
  return <div className={classes.profile_card}>{children}</div>;
}
