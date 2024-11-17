document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("jokesForm");
  const output = document.getElementById("output");

  form.addEventListener("submit", async (event) => {
      event.preventDefault();
      output.innerHTML = "";

      const language = document.getElementById("language").value;
      const category = document.getElementById("category").value;
      const number = document.getElementById("number").value;
      const jokeId = document.getElementById("jokeId").value;

      let url = "";

      if (jokeId) {
          url = `https://jokes-api-hq2a.onrender.com/api/v1/jokes/${jokeId}`;
      } else if (number) {
          url = `https://jokes-api-hq2a.onrender.com/api/v1/jokes/${language}/${category}/${number}`;
      } else {
          url = `https://jokes-api-hq2a.onrender.com/api/v1/jokes/${language}/${category}`;
      }

      try {
          const response = await fetch(url);

          if (!response.ok) {
              throw new Error(`Error: ${response.statusText}`);
          }

          const data = await response.json();
          if (data.jokes) {
              const jokes = Array.isArray(data.jokes) ? data.jokes : [data.jokes];
              jokes.forEach((joke) => {
                  const p = document.createElement("p");
                  p.textContent = joke;
                  p.classList.add("content");
                  output.appendChild(p);
              });
          } else if (data.error) {
              output.innerHTML = `<p class="has-text-danger">${data.error}</p>`;
          }
      } catch (error) {
          output.innerHTML = `<p class="has-text-danger">Failed to fetch jokes. ${error.message}</p>`;
      }
  });
});
