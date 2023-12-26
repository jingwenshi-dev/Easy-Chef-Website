import { Dropdown } from "react-bootstrap";

const Profile = ({ email, phone }) => {
    return (
        <>
            <Dropdown.Item>{email}</Dropdown.Item>
            <Dropdown.Item>{phone}</Dropdown.Item>
        </>
    )
}
export default Profile;