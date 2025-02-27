class TestLogEndpoints:
    def test_create_log_success(self, client, auth_headers, test_log_data):
        response = client.post("/v1/logs", json=test_log_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["fish_name"] == test_log_data["fish_name"]

    def test_create_log_missing_required(self, client, auth_headers, test_log_data):
        data = test_log_data.copy()
        del data["fish_name"]
        response = client.post("/v1/logs", json=data, headers=auth_headers)
        assert response.status_code == 422

    def test_get_log_success(self, client, auth_headers, test_log_data):
        # Create a log first
        create_response = client.post("/v1/logs", json=test_log_data, headers=auth_headers)
        log_id = create_response.json()["id"]
        
        response = client.get(f"/v1/logs/{log_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["fish_name"] == test_log_data["fish_name"]

    def test_update_log_success(self, client, auth_headers, test_log_data):
        # Create a log first
        create_response = client.post("/v1/logs", json=test_log_data, headers=auth_headers)
        log_id = create_response.json()["id"]
        
        update_data = {"fish_name": "Updated Fish Name"}
        response = client.put(f"/v1/logs/{log_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["fish_name"] == update_data["fish_name"]

    def test_filter_logs(self, client, auth_headers):
        response = client.get("/v1/logs/filter", headers=auth_headers, params={
            "fish_name": "Bass",
            "min_weight": 1.0,
            "released": True
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_delete_log_success(self, client, auth_headers, test_log_data):
        # Create a log first
        create_response = client.post("/v1/logs", json=test_log_data, headers=auth_headers)
        log_id = create_response.json()["id"]
        
        response = client.delete(f"/v1/logs/{log_id}", headers=auth_headers)
        assert response.status_code == 200

    def test_unauthorized_access(self, client, test_log_data):
        response = client.post("/v1/logs", json=test_log_data)
        assert response.status_code == 401
