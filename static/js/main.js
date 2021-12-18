const responsive = {
  0: {
    items: 1,
  },
  320: {
    items: 1,
  },
  560: {
    items: 2,
  },
  960: {
    items: 3,
  },
};

$(document).ready(function () {
  $(function () {
    setNavigationActive();
  });

  $nav = $(".nav");
  $toggleCollapse = $(".toggle-collapse");

  /** click event on toggle menu */
  $toggleCollapse.click(function () {
    $nav.toggleClass("collapse");
  });

  // owl-crousel for blog
  $(".owl-carousel").owlCarousel({
    loop: true,
    autoplay: false,
    autoplayTimeout: 3000,
    dots: false,
    nav: true,
    navText: [
      $(".owl-navigation .owl-nav-prev"),
      $(".owl-navigation .owl-nav-next"),
    ],
    responsive: responsive,
  });

  // click to scroll top
  $(".move-up span").click(function () {
    $("html, body").animate(
      {
        scrollTop: 0,
      },
      1000
    );
  });

  // AOS Instance
  AOS.init();

  // Loading comments

  // function load_comment(url) {
  //     $.ajax({
  //         method: 'GET',
  //         url: url,
  //         success: function (data) {
  //             // console.log(data);
  //             var i = 0;

  //             for (i; i <= data.length; i++) {

  //                 console.log(data[i]);
  //                 if (!data[i] == undefined) {
  //                     $("#comment-list").append(`<div class="comment"><h3>${data[i].name}</h3> <strong><span>${data[i].created_on}</span></strong><p class="comment-content">${data[i].body}</p><hr></div>`);
  //                     alert("comment loaded")
  //                 }

  //             }

  //         },
  //         error: function (error_data) {
  //             console.log(error_data);
  //             $("#comment-list").innerHTML += "<h2>Unable to load comments</h2>"
  //         },
  //         timeout: 5000
  //     })
  // };
  // setTimeout(function () {
  //     var url = $("#comment-list").data("url");
  //     console.log("loading comments")
  //     load_comment(url);
  // }, 2000)

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
      preConfirm: (login) => {
        console.log(login);
        if (login !== "") {
          console.log("Searchable term");
          var url = $("#search").data("url");
          return (window.location.href = `${url}?q=${login}`);
        } else {
        }
      },
    }).catch((error) => {
      Swal.showValidationMessage(`Andika ikintu ushakisha`);
    });
  }
  $(".search").click(function () {
    searchTerm();
  });

  //   end search

  // Setting active classess

  function setNavigationActive() {
    var path = window.location.pathname;
    path = decodeURIComponent(path);
    $(".nav-items li a").each(function () {
      var href = $(this).attr("href");
      if (path.substring(0, href.length) === href && href.length > 1) {
        $(this).addClass("active");
      } else if (window.location.pathname == "/") {
        $("#home").addClass("active");
      }
    });
  }
});
