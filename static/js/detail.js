$(document).ready(function () {
  (function ($) {
    $.postCSRF = function (url, data, callback, type) {
      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
      }

      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          var cookies = document.cookie.split(";");
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == name + "=") {
              cookieValue = decodeURIComponent(
                cookie.substring(name.length + 1)
              );
              break;
            }
          }
        }
        return cookieValue;
      }

      var csrftoken = getCookie("csrftoken");

      // shift arguments if data argument was omitted
      if ($.isFunction(data)) {
        type = type || callback;
        callback = data;
        data = undefined;
      }

      return $.ajax(
        jQuery.extend(
          {
            url: url,
            type: "POST",
            dataType: type,
            data: data,
            success: callback,
            beforeSend: function (xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
            },
          },
          jQuery.isPlainObject(url) && url
        )
      );
    };
  })(jQuery);

  jQuery(document).ready(function ($) {
    // use the template tags in our JavaScript call
    $.postCSRF("{{ hitcount.ajax_url }}", { hitcountPK: "{{ hitcount.pk }}" })
      .done(function (data) {
        //$('.post-views').text(data.hit_counted).attr('id', 'hit-counted-value').appendTo('#post-views');
        //alert(data.hit_counted);
        //$('#post-views').text(data.hit_message);
        // console.log(data)
      })
      .fail(function (data) {
        // console.log('POST failed');
        //console.log(data);
      });
  });

  const loadComments = () => {
    let commentDiv = document.getElementById("comment-list");
    let url = commentDiv.getAttribute("data-url");
    //console.log(url)
    $.ajax({
      url: url,
      method: "GET",
      success: (data) => {
        //console.log(data)
        if (data.length == 0) {
          commentDiv.innerHTML = `
                      <div class="comment">
                          <h3>Ba uwa mbere mugutanga ibitekerezo</h3>
                          <hr>
                      </div>
                      `;
        } else {
          //console.log("Data length:", data.length);
          commentDiv.innerHTML = "";
          data.forEach((comment) => {
            let date = new Date(comment.created_on);
            //console.log(date.toDateString())
            let commentElement = `
                          <div class="comment">
                              <h3>By ${
                                comment.name
                              }</h3> <strong><span>${date.toDateString()}</span></strong>
                              <p class="comment-content">${comment.body}</p>
                              
                          </div>
                          
                          `;
            commentDiv.innerHTML += commentElement;
          });
        }
      },
      error: (err) => {
        console.log(err);
        commentDiv.innerHTML = `
                  <div class="comment">
                      <h3>Ba uwa mbere mugutanga ibitekerezo</h3>
                      <hr>
                  </div>
                  `;
      },
      timeout: 6000,
    });
  };
  setTimeout(() => {
    loadComments();
  }, 2000);

  const saveComment = () => {
    let commentForm = document.querySelector(".comment-form");
    let url = commentForm.getAttribute("data-link");
    commentForm.addEventListener("submit", (e) => {
      e.preventDefault();

      let data = $(".comment-form").serializeArray();
      let formData = new FormData(commentForm);
      let token = data[0].value;
      let name = $("#comment-name").val();
      let email = $("#comment-email").val();
      let body = $("#comment-body").val();
      let bot = $("#comment-bot").val();
      const emailPattern = /\S+@\S+\.\S+/;
      //console.log(url)
      if (!bot == "none") {
        console.log("Probably a bot");

        Swal.fire({
          title: "Siga umwanya mo ubusa",
          icon: "error",
        });
      } else if (
        !email.match(emailPattern) ||
        body.length < 5 ||
        name.length < 2
      ) {
        Swal.fire({
          title: "Uzuza ahasabwa hose",
          icon: "error",
        });
      } else {
        let formdata = {
          csrfmiddlewaretoken: token,
          name: name,
          email: email,
          body: body,
        };
        $.ajax({
          url: url,
          method: "POST",
          data: formdata,
          success: (data) => {
            if (data.created == "true") {
              loadComments();
              Swal.fire({
                title: "Igitekerezo cyawe cyemewe",
                icon: "success",
              });
            } else {
              // console.log("Not created");
            }
            commentForm.reset();
            $(".comment.section").toggle(200);
          },
          error: (err) => {
            console.log(err);
            alert("Something happened on our end");
          },
        });
      }
    });
  };
  saveComment();

  const postLike = () => {
    $("#post-like-button").click((e) => {
      e.preventDefault();
      let postId = $("#post-like-button").data("post");

      let currentLikePosts = localStorage.getItem("likedPosts");
      if (!currentLikePosts) {
        localStorage.setItem("likedPosts", JSON.stringify({ 0: new Date() }));
        currentLikePosts = localStorage.getItem("likedPosts");
      }
      // console.log(currentLikePosts)
      if (postId) {
        if (currentLikePosts) {
          currentLikePosts = JSON.parse(currentLikePosts);
        }
        if (currentLikePosts[postId]) {
        } else {
          currentLikePosts[postId] = new Date();
          //console.log(currentLikePosts)
          localStorage.setItem("likedPosts", JSON.stringify(currentLikePosts));
          Swal.fire({
            title: "Post added to your liked",
            icon: "success",
          });
          let url = $("#post-like-button").data("url");
          $.ajax({
            url: url,
            method: "GET",
            success: (data) => {
              if (data.likes) {
                console.log("Logged");
                $(".post-likes").text(data.likes);
              }
            },
            error: (err) => {
              console.log(err);
            },
          });
          checkLike(postId);
        }
      } else {
        console.log("Something is missing: ", postId, currentLikePosts);
      }
    });
  };
  const checkLike = (postId) => {
    let likedPosts = localStorage.getItem("likedPosts");
    //console.log("Checking", postId)
    if (likedPosts) {
      let posts = JSON.parse(likedPosts);
      //console.log(posts)
      Object.keys(posts).forEach((post) => {
        if (post == postId) {
          $("#post-like-button").removeAttr("data-post");
          $("#post-like-button").html("<b>Liked</b>");
        }
      });
    } else {
    }
  };

  postLike();
  checkLike($("#post-like-button").data("post"));
});
