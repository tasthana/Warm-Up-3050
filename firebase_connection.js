// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBtYMOxZ-iTXIl71HGpslMO_AVqF8MYh4c",
  authDomain: "warm-up-project-3050.firebaseapp.com",
  projectId: "warm-up-project-3050",
  storageBucket: "warm-up-project-3050.appspot.com",
  messagingSenderId: "1009167844235",
  appId: "1:1009167844235:web:360b0daeb2774a141b258e",
  measurementId: "G-6LDR0JPTNZ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);


var admin = require("firebase-admin");

var serviceAccount = require("Desktop/warm-up-project-3050.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
