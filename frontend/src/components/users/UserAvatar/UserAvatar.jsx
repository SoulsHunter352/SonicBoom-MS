import userPicture from "../../../assets/images/noAvatar.webp";
import classes from "./UserAvatar.module.css";

export default function UserAvatar() {
  return (
    <div className={classes.wrapper}>
      <img className={classes.avatar} src={userPicture} />
    </div>
  );
}
