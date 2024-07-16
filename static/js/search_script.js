const displayData = (contacts) => {
  contacts.forEach((contact) => {
    const contactTableRow = document.createElement("tr");
    const contactNameCell = document.createElement("td");
    const companyCell = document.createElement("td");
    const regionCell = document.createElement("td");
    const telephoneCell = document.createElement("td");
    const mobilephoneCell = document.createElement("td");

    contactNameCell.innerText = contact.name;
    companyCell.innerText = contact.company;
    regionCell.innerText = contact.region;
    telephoneCell.innerText = contact.telephone_number;
    mobilephoneCell.innerText = contact.mobile_phone_number;

    contactTableRow.appendChild(contactNameCell);
    contactTableRow.appendChild(companyCell);
    contactTableRow.appendChild(regionCell);
    contactTableRow.appendChild(telephoneCell);
    contactTableRow.appendChild(mobilephoneCell);

    contactTableBody.appendChild(contactTableRow);
  });
};

const searchQueryInput = document.getElementById("search-query");

const searchQuery = (e) => {
  while (contactTableBody.firstChild) {
    contactTableBody.removeChild(contactTableBody.firstChild);
  }

  const query = searchQueryInput.value;
  const url = "/search";
  const urlQuery = url + `?search_query=${query}`;
  fetch(urlQuery, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      displayData(data);
    });
};

const getAllContacts = () => {
  const url = "/search";
  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      displayData(data);
    });
};

const contactTableBody = document.getElementById("contact-table-body");
document.addEventListener("DOMContentLoaded", getAllContacts);
searchQueryInput.addEventListener("input", searchQuery);
