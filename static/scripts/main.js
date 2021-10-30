$(document).ready(function () {
  //   search button
  function searchTerm() {
    Swal.fire({
      title: "Shakisha",
      input: "text",
      inputAttributes: {
        autocapitalize: "on",
      },
      showCancelButton: true,
      confirmButtonText: "Shaka",
      showLoaderOnConfirm: true,
      //     preConfirm: (login) => {
      //       return fetch(`//api.github.com/users/${login}`)
      //         .then(response => {
      //           if (!response.ok) {
      //             throw new Error(response.statusText)
      //           }
      //           return response.json()
      //         })
      //         .catch(error => {
      //           Swal.showValidationMessage(
      //             `Request failed: ${error}`
      //           )
      //         })
      //     },
      //     allowOutsideClick: () => !Swal.isLoading()
      //   }).then((result) => {
      //     if (result.isConfirmed) {
      //       Swal.fire({
      //         title: `${result.value.login}'s avatar`,
      //         imageUrl: result.value.avatar_url
      //       })
      //     }
    });
  }
  $(".search").click(function () {
    searchTerm();
  });
  $(".coming-soon").click(function () {
    let timerInterval;

    Swal.fire({
      title: "Biraza vuba",
      html: "Iki gice turi kugikora. Kirahagera vuba",
      timer: 2000,
      timerProgressBar: false,
      position: "bottom-end",
      didOpen: () => {
        Swal.showLoading();
        const b = Swal.getHtmlContainer().querySelector("b");
        timerInterval = setInterval(() => {
          b.textContent = Swal.getTimerLeft();
        }, 100);
      },
      willClose: () => {
        clearInterval(timerInterval);
      },
    }).then((result) => {
      /* Read more about handling dismissals below */
      if (result.dismiss === Swal.DismissReason.timer) {
        console.log("I was closed by the timer");
      }
    });
  });
});
