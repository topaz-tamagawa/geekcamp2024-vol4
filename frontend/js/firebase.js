import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAuth, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-analytics.js";

export { sendSignInLinkToEmail, isSignInWithEmailLink, signInWithEmailLink, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyDfBvthpqiOCsJDAH08SDtUeKFwDBzOmxE",
  authDomain: "geekcamp2024-vol4-topaz.firebaseapp.com",
  projectId: "geekcamp2024-vol4-topaz",
  storageBucket: "geekcamp2024-vol4-topaz.appspot.com",
  messagingSenderId: "381501157126",
  appId: "1:381501157126:web:5df2198379e53c9579b887",
  measurementId: "G-CTV6WBYQYM"
};


/** @type {import("firebase/app").FirebaseApp}  */
export const firebase = initializeApp(firebaseConfig);
/** @type {import("firebase/firestore").Firestore}  */
export const firestore = getFirestore(firebase);
/** @type {import("firebase/auth").Auth}  */
export const auth = getAuth(firebase);
/** @type {import("firebase/analytics").Analytics}  */
export const analytics = getAnalytics(firebase);

export const providers = {
  google: new GoogleAuthProvider()
}
