db.createUser({
        user: "dbadmin",
        pwd: "dbadmin",
        roles: [
            {
                role: "readWrite",
                db: "admin"
            },
            {
                role: "readWrite",
                db: "test"
            }
        ]
});


