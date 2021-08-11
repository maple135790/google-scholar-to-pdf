class ScholarScrap {
  constructor(query, MAX_PAGE) {
    this.query = query;
    this.maxPage = MAX_PAGE;
  }
  save() {
    var iframes = document.getElementsByTagName("iframe").length;
    for (var i = 0; i < iframes; i++) {
      var filename =
        this.query +
        "-" +
        i
          .toLocaleString("en-US", {
            minimumIntegerDigits: 2,
            useGrouping: false,
          })
          .toString() +
        ".html";
      var data =
        document.getElementsByTagName("iframe")[i].contentWindow.document
          .documentElement.innerHTML;

      if (typeof data === "object") {
        data = JSON.stringify(data, undefined, 4);
      }

      var blob = new Blob([data], { type: "text/json" }),
        e = document.createEvent("MouseEvents"),
        a = document.createElement("a");

      a.download = filename;
      a.href = window.URL.createObjectURL(blob);
      a.dataset.downloadurl = ["text/json", a.download, a.href].join(":");
      e.initMouseEvent(
        "click",
        true,
        false,
        window,
        0,
        0,
        0,
        0,
        0,
        false,
        false,
        false,
        false,
        0,
        null
      );
      a.dispatchEvent(e);
    }
  }
  scrap() {
    var MAX_PAGE = this.maxPage;
    var query = this.query;
    var d = document;
    var url = "https://scholar.google.com/scholar?q=" + query;
    var isHostSame = false;
    function sleepByPromise(millisec) {
      return new Promise((resolve) => setTimeout(resolve, millisec));
    }
    async function wait(millisec) {
      await sleepByPromise(millisec);
    }
    if (window.location.host != "scholar.google.com") {
      if (window.confirm("go to Google Scholar"))
        location.href = "https://scholar.google.com/";
    } else {
      isHostSame = true;
    }
    if (isHostSame) {
      for (var page = 0; page < MAX_PAGE; page++) {
        var newPage = d.createElement("iframe");
        newPage.src = url + "&start=" + (page * 10).toString();
        d.getElementsByTagName("body")[0].appendChild(newPage);
        wait(500);
      }
    }
  }
}
