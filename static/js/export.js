$.fn.exportToExcel = function (table) {
  self = $(this);
  self.html("Processing...");
  self.addClass(
    "kt-spinner kt-spinner--v2 kt-spinner--right kt-spinner--md kt-spinner--warning"
  );

  var info = table.page.info();
  if (info.recordsTotal > self.data("max-row-length")) {
    setTimeout(function () {
      $.ajax({
        url: self.data("async-url"),
        type: "GET",
        success: function (response) {
          str =
            "Process ID " +
            response.task_id +
            " has been queued. We'll notify you once it's done.";
          toastr.success(str);
          self.removeClass(
            "kt-spinner kt-spinner--v2 kt-spinner--right kt-spinner--md kt-spinner--warning"
          );
          self.html("Download Data");
        },
      });
    }, 100);
  } else {
    window.location.href = self.data("non-async-url");
    self.removeClass(
      "kt-spinner kt-spinner--v2 kt-spinner--right kt-spinner--md kt-spinner--warning"
    );
    self.html("Download Data");
  }
};
