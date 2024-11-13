"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


app.data = {    
    data: function() {
        return {
            contacts: [],
            new_contact: { name: "", affiliation: "", description: "", contact_image: "https://bulma.io/assets/images/placeholders/96x96.png" },
            edit_contact: null
        };
    },
    methods: {
        // Complete. 
        loadContacts() {
            fetch(get_contacts_url)
            .then(response =>response.json())
            .then(data => {
                console.log("Contacts from GET:", data.contacts);
                this.contacts = data.contacts;
            });
        },

        addContact() {
            fetch(add_contact_url, {
                method: "POST",
                headers: { "Content-Type" : "application/json" },
                body: JSON.stringify(this.new_contact)
            })
            .then(response =>response.json())
            .then(data => {
                if (data.contact_id) {
                    this.contacts.push({ ...this.new_contact, id: data.contact_id });
                    this.resetContact();
                    console.log("Contact added with ID:", data.contact_id);
                    this.loadContacts();
                }
                else{
                    console.error("Error adding contact: ", data);
                }
            })
            .catch(error => {
                console.error("Server error: ", error);
            });
        },

        resetContact() {
            this.new_contact = { name: "", affiliation: "", description: "", contact_image: "https://bulma.io/assets/images/placeholders/96x96.png" };
        },

        deleteContact(contact) {
            fetch(`${delete_contact_url}/${contact.id}`, { method: "DELETE" })
                .then(() => {
                    this.contacts = this.contacts.filter(c => c.id !== contact.id);
                });
        },
        
        editField(contact, field) {
            contact.editing = field;
        },

        saveField(contact, field) {
            fetch(`${update_contact_url}/${contact.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ [field]: contact[field] })
            }) 
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    console.log('Field ${field} updated for Contact ID: ${contact.id}');
                    contact.editing = null;
                }
                else {
                    console.error("Error updating contact:", data);
                }
            })
            .catch(error => console.error("Error updating field: ", error));
        },

        pickImage(contact) {
            let input = document.getElementById("file-input");
            input.onchange = () => {
                let file = input.files[0];
                if (file) {
                    const formData = new FormData();
                    formData.append("photo", file);
                    fetch(`${upload_photo_url}/${contact.id}`, {
                        method: "POST",
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.photo_url) {
                            contact.photo_url = data.photo_url;
                            console.log('Image updated for contact ID: ${contact.id}');
                        }
                    })
                    .catch(error => console.error("Error uploading image:", error))
                }
            };
            input.click();
        }
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    // Complete.
    app.vue.loadContacts();
}

app.load_data();

