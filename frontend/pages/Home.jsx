import { userAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";


export default function Home() {
    const { user, logout } = userAuth();
    const navigate = useNavigate();

    const handleLogin = () => navigate("/login")
    const handleSignup = () => navigate("/signup")

    return (
        <div>

        </div>
    )
}
