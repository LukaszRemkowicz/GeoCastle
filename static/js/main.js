// import { IMAGE_API_KEY } from "./ApiKey";

$("#user-menu").click(function () {
  $("#drop-menu").toggle();
});

console.log("work");

const scriptTag =
  "<script>" +
  "function sendId() {const text = $('b').attr('id'); window.parent.postMessage(text); $(function(){$('.leaflet-popup-close-button').click(function(){window.parent.postMessage('close');});});};" +
  "</script>";

cleanInfo = () => {
  $("#castle-name").text("");
  $("#castle-type").text("");
  $("#castle-website").text("");
  $(`#castle-photo-1 > img`).attr("src", "");
  $(`#castle-photo-2 > img`).attr("src", "");
  $(`#castle-photo-3 > img`).attr("src", "");
  $('input[name="current-state"]').prop("checked", false);
  $("#review").val("");
};

$("iframe").contents().find("body").append(scriptTag);
$(document).ready(function () {
  $("#close-btn").click(function () {
    $(".infobox").hide();
  });
});

const iframe = document.getElementsByTagName("iframe")[0];
let iWindow = null;

window.addEventListener("message", (event) => {
  const { data } = event;
  if (data === "close") {
    $(".infobox").hide();
  } else {
    $.ajax({
      method: "GET",
      data: { castle_id: data }, //loc_id: data },
      success: function (resp) {
        cleanInfo();
        $("#castle-name").text(resp.name);
        const requestName = imageName(resp.name);
        const imagesRequest = settings(requestName);
        $.ajax(imagesRequest).done(function (response) {
          //console.log(response);
          response.value.map((val, index) => {
            $(`#castle-photo-${index + 1} > img`).attr("src", val.url);
          });
        });
        $("#castle-type").text(resp.castle_type);
        $("#castle-website").text(resp.website);
        $(".infobox").show();
      },
    });
  }
});

imageName = (name) => {
  let flatName = name.toLowerCase();
  let readyName = flatName.split(" ").join("%20");
  return readyName;
};

function showReviewBox() {
  $("#review-area").show();
}

function hideReviewBox() {
  $("#review-area").hide();
}

var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  },
});

$("#submit-btn").click(function () {
  const castleName = $("#castle-name").text();
  const state = $('input[name="current-state"]:checked').val();
  const review = $("#review").val();

  $.ajax({
    method: "POST",
    data: { castleName: castleName, state: state, review: review },
    success: function () {
      cleanInfo();
      $(".infobox").hide();
      //location.reload();
    },
  });
});

settings = (requestName) => ({
  async: true,
  crossDomain: true,
  url: `https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI?q=${requestName}&pageNumber=1&pageSize=3&autoCorrect=false`,
  method: "GET",
  headers: {
    "x-rapidapi-key": "",
    "x-rapidapi-host": "contextualwebsearch-websearch-v1.p.rapidapi.com",
  },
});
