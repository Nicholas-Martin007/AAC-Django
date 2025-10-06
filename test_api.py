import requests
import json

BASE_URL = "http://localhost:8000/api/kartu/"


def create_card():
    data = {
        "label": "Test Card",
        "gambar": '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red"/></svg>',
    }
    response = requests.post(BASE_URL, json=data)
    print("Created:", response.json())
    return response.json()["kartu_id"]


def get_all_cards():
    response = requests.get(BASE_URL)
    print("All cards:", response.json())


def get_card(card_id):
    response = requests.get(f"{BASE_URL}{card_id}/")
    print("Single card:", response.json())


def update_card(card_id):
    data = {
        "label": "Updated Test Card",
        "gambar": '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="blue"/></svg>',
    }
    response = requests.put(f"{BASE_URL}{card_id}/", json=data)
    print("Updated:", response.json())


def delete_card(card_id):
    response = requests.delete(f"{BASE_URL}{card_id}/")
    print("Deleted:", response.json())


if __name__ == "__main__":
    # Test all CRUD operations
    print("Testing CRUD operations...")

    # Create
    card_id = create_card()

    # Read
    get_all_cards()
    get_card(card_id)

    # Update
    update_card(card_id)

    # Verify update
    get_card(card_id)

    # Delete
    delete_card(card_id)

    # Verify deletion
    get_all_cards()
