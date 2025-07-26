import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";


const firebaseConfig = {
    apiKey: "AIzaSyCqkkqb4LsD1iJ1x2WDAYC7Rd_6LQhb5bE",
    authDomain: "reverse-sell.firebaseapp.com",
    projectId: "reverse-sell",
    storageBucket: "reverse-sell.firebasestorage.app",
    messagingSenderId: "861620980484",
    appId: "1:861620980484:web:194c52c8d8eedf568c5e51",
    measurementId: "G-Y5EJ80Y452"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider };
