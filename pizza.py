import pandas as pd

# Step 1: Load the CSV files
pizzas_df = pd.read_csv('pizzas.csv', encoding='latin-1')
orders_df = pd.read_csv('orders.csv', encoding='latin-1')
order_details_df = pd.read_csv('order_details.csv', encoding='latin-1')
pizza_types_df = pd.read_csv('pizza_types.csv', encoding='latin-1')

# Debug: Print column names to verify structure
print("Columns in pizzas_df:", pizzas_df.columns.tolist())
print("Columns in orders_df:", orders_df.columns.tolist())
print("Columns in order_details_df:", order_details_df.columns.tolist())
print("Columns in pizza_types_df:", pizza_types_df.columns.tolist())

# Step 2: Data cleaning and preparation
# Convert date and time to datetime
orders_df['datetime'] = pd.to_datetime(orders_df['date'] + ' ' + orders_df['time'])
orders_df['date'] = pd.to_datetime(orders_df['date'])
orders_df['hour'] = orders_df['datetime'].dt.hour

# Merge datasets
merged_df = order_details_df.merge(pizzas_df, on='pizza_id', how='left')
merged_df = merged_df.merge(orders_df, on='order_id', how='left')
merged_df = merged_df.merge(pizza_types_df, on='pizza_type_id', how='left')

# Debug: Print merged_df columns to verify
print("Columns in merged_df:", merged_df.columns.tolist())

# Check and rename 'price' column if it has a different name
if 'price' not in merged_df.columns:
    price_candidates = [col for col in merged_df.columns if 'price' in col.lower()]
    if price_candidates:
        merged_df.rename(columns={price_candidates[0]: 'price'}, inplace=True)
        print(f"Renamed {price_candidates[0]} to 'price'")
    else:
        raise KeyError("No 'price' or similar column found in merged_df. Check pizzas.csv structure.")

# Calculate total price per order item
merged_df['total_price'] = merged_df['quantity'] * merged_df['price']

# Step 3: Basic analysis
# Total revenue
total_revenue = merged_df['total_price'].sum()
print(f"Total Revenue: ${total_revenue:.2f}")

# Top 5 pizza types by quantity sold
top_pizzas = merged_df.groupby('pizza_type_id')['quantity'].sum().sort_values(ascending=False).head(5)
print("\nTop 5 Pizza Types by Quantity Sold:")
print(top_pizzas)

# Orders by hour
orders_by_hour = merged_df.groupby('hour')['order_id'].nunique()

# Step 4: Chart.js-compatible charts
# Chart 1: Top 5 Pizza Types by Quantity Sold (Bar Chart)
top_pizza_data = top_pizzas.reset_index()
chart1 = {
  "type": "bar",
  "data": {
    "labels": top_pizza_data['pizza_type_id'].tolist(),
    "datasets": [{
      "label": "Quantity Sold",
      "data": top_pizza_data['quantity'].tolist(),
      "backgroundColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
      "borderColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
      "borderWidth": 1
    }]
  },
  "options": {
    "scales": {
      "y": {
        "beginAtZero": True,
        "title": {
          "display": True,
          "text": "Quantity Sold"
        }
      },
      "x": {
        "title": {
          "display": True,
          "text": "Pizza Type"
        }
      }
    },
    "plugins": {
      "title": {
        "display": True,
        "text": "Top 5 Pizza Types by Quantity Sold"
      }
    }
  }
}
print("\nChart 1: Top 5 Pizza Types by Quantity Sold")
print(chart1)

# Chart 2: Orders by Hour (Line Chart)
chart2 = {
  "type": "line",
  "data": {
    "labels": orders_by_hour.index.tolist(),
    "datasets": [{
      "label": "Number of Orders",
      "data": orders_by_hour.values.tolist(),
      "backgroundColor": "rgba(255, 127, 14, 0.2)",
      "borderColor": "#ff7f0e",
      "borderWidth": 2,
      "fill": True,
      "tension": 0.1
    }]
  },
  "options": {
    "scales": {
      "y": {
        "beginAtZero": True,
        "title": {
          "display": True,
          "text": "Number of Orders"
        }
      },
      "x": {
        "title": {
          "display": True,
          "text": "Hour"
        }
      }
    },
    "plugins": {
      "title": {
        "display": True,
        "text": "Orders by Hour of Day"
      }
    }
  }
}
print("\nChart 2: Orders by Hour of Day")
print(chart2)

# Step 5: Business recommendations
print("\nBusiness Recommendations:")
print("1. Focus marketing on the top 5 pizza types to maximize sales.")
print("2. Target promotions during peak hours (e.g., late afternoon to evening) based on the orders by hour chart.")
print("3. Consider analyzing underperforming pizza types for potential menu adjustments.")