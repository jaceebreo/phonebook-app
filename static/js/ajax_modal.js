var ajax_modal = $("#ajax-modal");
var ajax_modal_body = ajax_modal.find("div.modal-body");
var ajax_table = $("#ajax-table");

$.fn.submitAjaxForm = function () {
  $(this).submit(function (e) {
    var self = $(this);

    e.preventDefault();

    var save_btn_label = $("#ajax-modal").find("button[type=submit]").html();

    $("#ajax-modal").find("button[type=submit]").attr("disabled", "disabled");
    $("#ajax-modal")
      .find("button[type=submit]")
      .html("<i class='fal fa-spinner fa-spin'></i> Processing...");

    $.ajax({
      url: self.attr("action"),
      type: "POST",
      data: new FormData(self[0]),
      processData: false,
      contentType: false,
      success: function (response) {
        if (response.success) {
          if (self.data("ajax-modal-refresh-on-success")) {
            location.reload();
          } else {
            ajax_modal.modal("hide");
            if (response.message) {
              if (response.message_status == "success") {
                toastr.success(response.message);
              } else if (response.message_status == "info") {
                toastr.info(response.message);
              } else if (response.message_status == "warning") {
                toastr.warning(response.message);
              } else if (response.message_status == "error") {
                toastr.error(response.message);
              } else {
                toastr.success(response.message);
              }
            }

            if (typeof table != "undefined") {
              table.ajax.reload();
            }

            ajax_modal_body
              .empty()
              .html(response)
              .find("form")
              .attr("action", self.attr("action"))
              .submitAjaxForm();
            $(this).find("form button[type=submit]").removeAttr("disabled");
          }
        }
      },
      error: function (response) {
        if (response.responseJSON) {
          $.each(response.responseJSON, function (error_key, errors) {
            with_formset = response.responseJSON.with_formset;

            if (errors) {
              if (with_formset) {
                error_html = JSON.stringify(errors);
                ajax_modal_body.find("#errors").show().html(error_html);
              } else {
                error_html = "<ul>";
                errors = JSON.parse(errors);
                $.each(errors, function (key, messages) {
                  $.each(messages, function (key1, val) {
                    error_html += "<li>" + key + " - " + val.message + "</li>";
                  });
                  error_html += "</ul>";
                });
                ajax_modal_body.find("#errors").show().html(error_html);
              }
            }
          });

          $("#ajax-modal")
            .find("button[type=submit]")
            .removeAttr("disabled", "disabled");
          $("#ajax-modal").find("button[type=submit]").html(save_btn_label);
        }
      },
    });
  });
  return this;
};

$.fn.displayAjaxModal = function () {
  var self = $(this);
  ajax_modal.find(".modal-title").html(self.data("ajax-modal-title"));

  if (self.data("ajax-modal-lg")) {
    ajax_modal.find(".modal-lg").attr("class", "modal-dialog modal-xl");
  } else {
    ajax_modal.find(".modal-xl").attr("class", "modal-dialog modal-lg");
  }

  $.ajax({
    url: self.data("ajax-modal-url"),
    type: "GET",
    success: function (response) {
      ajax_modal_body
        .empty()
        .html(response)
        .find("form")
        .attr("action", self.data("ajax-modal-url"))
        .attr(
          "data-ajax-modal-refresh-on-success",
          self.data("ajax-modal-refresh-on-success")
        )
        .submitAjaxForm();
      ajax_modal.modal("show");
    },
  });
};

$.fn.hookAjaxModal = function () {
  $(this).click(function (e) {
    var self = $(this);
    ajax_modal.find(".modal-title").html(self.data("ajax-modal-title"));

    if (self.data("ajax-modal-lg")) {
      ajax_modal.find(".modal-lg").attr("class", "modal-dialog modal-xl");
    } else {
      ajax_modal.find(".modal-xl").attr("class", "modal-dialog modal-lg");
    }

    $.ajax({
      url: self.data("ajax-modal-url"),
      type: "GET",
      success: function (response) {
        ajax_modal_body
          .empty()
          .html(response)
          .find("form")
          .attr("action", self.data("ajax-modal-url"))
          .attr(
            "data-ajax-modal-refresh-on-success",
            self.data("ajax-modal-refresh-on-success")
          )
          .submitAjaxForm();
        ajax_modal.modal("show");
      },
    });
  });
};

$.fn.submitBatchProcess = function (action_type, csrf_token, url, ajax_table) {
  $(this).click(function (e) {
    var self = $(this);
    e.preventDefault();

    var id_arr = [];
    ajax_table.$('input[type="checkbox"]').each(function () {
      if (this.checked) {
        id_arr.push(this.value);
      }

      if (!$.contains(document, this)) {
        if (this.checked) {
          $(form).append(
            $("<input>")
              .attr("type", "hidden")
              .attr("name", this.name)
              .val(this.value)
          );
        }
      }
    });

    var data = {};
    if (action_type == "update") {
      data = $(".mod-form").serializeArray();
      data.push({ name: "id_arr", value: id_arr });
    } else {
      data = {
        id_arr: id_arr,
        csrfmiddlewaretoken: csrf_token,
      };
    }

    $.ajax({
      url: url,
      type: "POST",
      data: data,
      success: function (response) {
        if (response.success) {
          ajax_modal.modal("hide");
          toastr.success("Recods updated successfully.");
          var rows = ajax_table.rows({ search: "applied" }).nodes();
          $('input[type="checkbox"]', rows).prop("checked", false);
          ajax_table.ajax.reload();
          $(".btn-batch-update").hide();
        } else {
          $("#error-msg").remove();
          html_errors = '<div id="error-msg" class="alert alert-danger"><ul>';
          li = "";
          $.each(response.form_errors, function (index, value) {
            li = li + "<li>" + value + "</li>";
          });
          html_errors = html_errors + li + "</ul></div>";
          ajax_modal_body.prepend(html_errors);
        }
      },
    });
  });
  return this;
};

var get_selected_checkbox = function (table) {
  var id_arr = [];
  table.$('input[type="checkbox"]').each(function () {
    if (this.checked) {
      id_arr.push(this.value);
    }

    if (!$.contains(document, this)) {
      if (this.checked) {
        $(form).append(
          $("<input>")
            .attr("type", "hidden")
            .attr("name", this.name)
            .val(this.value)
        );
      }
    }
  });

  return id_arr;
};

$.fn.displayBatchProcessAjaxModal = function (action_type, csrf_token) {
  var self = $(this);
  ajax_modal.find(".modal-title").html(self.data("ajax-modal-title"));

  var id_arr = get_selected_checkbox(table);
  $.ajax({
    url: self.data("ajax-modal-url"),
    type: "GET",
    data: {
      id_arr: id_arr,
    },
    success: function (response) {
      ajax_modal_body.empty().html(response);
      $(".btn-submit").submitBatchProcess(
        action_type,
        csrf_token,
        self.data("ajax-modal-url"),
        table
      );
      ajax_modal.modal("show");
    },
  });
  return false;
};
