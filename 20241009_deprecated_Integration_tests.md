# Tests d'intégration 

## 1. Endpoint /translation
```
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

var schema = {
    "username": {
        "type": "string"
    },
    "password": {
        "type": "string"
    },
    "email": {
        "type": "string"
    },
};

var Ajv = require('ajv') ; 

pm.test("Validate JSON Response Schema", () => {

  const response = pm.response.json();
  const isValid = Ajv().validate(schema, response);

  pm.expect(isValid).to.be.equal(true);
  if (!isValid) {
    pm.test.error(Ajv().errorsText());
  }
});
```

## 2. Endpoint /signup
```
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

var schema = {
    "username": {
        "type": "string"
    },
    "password": {
        "type": "string"
    },
    "email": {
        "type": "string"
    },
};

var Ajv = require('ajv') ; 

pm.test("Validate JSON Response Schema", () => {

  const response = pm.response.json();
  const isValid = Ajv().validate(schema, response);

  pm.expect(isValid).to.be.equal(true);
  if (!isValid) {
    pm.test.error(Ajv().errorsText());
  }
});
```
## 3. Endpoint /login 
```
pm.test("Body matches string", function () {
    pm.expect(pm.response.text()).to.include("bearer");
});

var schema = {
    "access_token": {
        "type": "string"
    },
    "token_type": {
        "type": "string"
    }
};
var Ajv = require('ajv') ; 

pm.test("Validate JSON Response Schema", () => {

  const response = pm.response.json();
  const isValid = Ajv().validate(schema, response);

  pm.expect(isValid).to.be.equal(true);
  if (!isValid) {
    pm.test.error(Ajv().errorsText());
  }
});

pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```
