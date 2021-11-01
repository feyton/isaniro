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
