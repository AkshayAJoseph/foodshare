import { Storage } from "@capacitor/storage";
import { App } from "@capacitor/app";
import { goto } from "$app/navigation";
import { Camera, CameraResultType, CameraSource } from "@capacitor/camera";
const baseUrl = "https://api.laddu.cc/api/v1";

async function setToken(token) {
  await Storage.set({
    key: "token",
    value: token,
  });
}

function handleBackButton(fallbackUrl) {
    if (typeof window !== "undefined" && typeof sessionStorage !== "undefined") {
      sessionStorage.setItem("fallbackPage", fallbackUrl);
  
      App.addListener("backButton", () => {
        const prevPage = sessionStorage.getItem("fallbackPage");
  
        if (
          window.location.href !== "https://localhost/" &&
          window.location.href !== "https://localhost/home"
        ) {
          goto(prevPage, { replaceState: true });
        } else {
          App.exitApp();
        }
      });
    } else {
    }
  }

  async function checkUser() {
    const { value } = await Storage.get({ key: "token" });
    console.log(value);
    if (!value) {
      goto("login", { replaceState: true });
      return;
    }
    const response = await fetch(`${baseUrl}/verify`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${value}`,
      },
    });
    const res = await response.json();
    if (!response.ok) {
      alert(res.message);
      await logout();
      goto("/login", { replaceState: true });
      return;
    }
    const id = res.id;
    const response2 = await fetch(`${baseUrl}/users/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const res2 = await response2.json();
    if (!response2.ok) {
      alert(res2.message);
      return;
    }
    console.log('done')
    return res2.data;
  }

  async function logout() {
    try {
      await Storage.remove({ key: "token" });
      goto("/login", { replaceState: true });
    } catch (error) {
      console.error("Error:", error);
    }
  }

  async function login(data) {
    try {
      console.log(data);
      const response = await fetch(`${baseUrl}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      const res = await response.json();
      if (!response.ok) {
        alert(res.message);
        return;
      }
      await setToken(res.token);
      goto("/home", { replaceState: true });
    } catch (error) {
      console.log(error);
    }
  }

  async function signup(data) {
    try {
      console.log(data);
      const response = await fetch(`${baseUrl}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      const res = await response.json();
      if (!response.ok) {
        alert(res.message);
        return;
      }
      await setToken(res.token);
      goto("/", { replaceState: true });
    } catch (error) {
      console.log(error);
    }
  }

  async function takephoto() {
    try {
      const image = await Camera.getPhoto({
        quality: 40,
        source: CameraSource.Camera, // Use "CameraSource.Photos" for gallery
        resultType: CameraResultType.Base64, // "Uri" returns the image URL
      });

      await runAI(image.base64String);
    } catch (error) {
      alert(error);
    }
  }

  async function runAI(base64) {
    try {
      const prompt =
        "if the image has any products in it send only a json containing {name,quantity,lifespan} lifespan being an estimate of the food life in hours, the quantity being the number of servings of the product in the picture, of all unique products seen in the picture";
      const model = genAI.getGenerativeModel({
        model: "gemini-1.5-pro",
        generationConfig: {
          response_mime_type: "application/json",
        },
      });
  
      console.log("t2");
  
      const imageParts = [
        {
          inlineData: {
            data: base64,
            mimeType: "image/jpeg",
          },
        },
      ];
  
      console.log("t3");
  
      const generatedContent = await model.generateContent([
        prompt,
        ...imageParts,
      ]);
  
      console.log("t4");
  
      const output = generatedContent.response.text();
      const out = JSON.parse(output);
      console.log(out);
      if (!out.products) {
        const response = await fetch(`${baseUrl}/food`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: out.name,
            quantity: Number(out.quantity),
            lifespan: Number(out.expiry),
          }),
        });
        const res = await response.json();
        if (!response.ok) {
          console.log(res);
          return;
        }
        // console.log(res);
        // const userdata = await checkUser();
        // const userid = userdata.id;
        // const id = res.data.id;
        // const response3 = await fetch(`${baseUrl}/ingredient/${userid}`, {
        //   method: "PUT",
        //   headers: {
        //     "Content-Type": "application/json",
        //   },
        //   body: JSON.stringify({
        //     ingid: id,
        //   }),
        // });
  
        // const res3 = await response3.json();
        // if (!response3.ok) {
        //   alert(res3.message);
        //   return;
        // }
        // console.log(res3);
  
        // alert("Product added");
        console.log(res)
        return;
      }
  
      const arr = out.products;
  
      const data = arr.map(async (d) => {
        const response = await fetch(`${baseUrl}/food`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: d.name,
            quantity: d.quantity,
            lifespan: d.lifespan,
          }),
        });
        const res = await response.json();
        if (!response.ok) {
          alert(res.message);
        }
        console.log(res);
      });
    } catch (error) {
      console.log(error);
    }
  }
  
  export {handleBackButton, checkUser, logout, login, signup, takephoto}