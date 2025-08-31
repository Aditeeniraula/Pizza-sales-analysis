import pandas as pd
import matplotlib.pyplot as plt

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
orders_df['day_of_week'] = orders_df['datetime'].dt.day_name()

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

# Handle missing values
merged_df['quantity'] = merged_df['quantity'].fillna(1)
merged_df['price'] = merged_df['price'].fillna(merged_df['price'].median())

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

# Additional analysis: Sales by category (using category_y)
merged_df['category'] = merged_df['category_y']  # Rename category_y to category for clarity
sales_by_category = merged_df.groupby('category')['total_price'].sum().sort_values(ascending=False)
print("\nTotal Sales by Category:")
print(sales_by_category)

# Orders by day of week
orders_by_day = merged_df.groupby('day_of_week')['order_id'].nunique().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
print("\nOrders by Day of Week:")
print(orders_by_day)

# Step 4: Visualizations
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
            "y": {"beginAtZero": True, "title": {"display": True, "text": "Quantity Sold"}},
            "x": {"title": {"display": True, "text": "Pizza Type"}}
        },
        "plugins": {"title": {"display": True, "text": "Top 5 Pizza Types by Quantity Sold"}}
    }
}
print("\nChart 1: Top 5 Pizza Types by Quantity Sold (for Canvas Panel)")
print(chart1)

# Matplotlib Visualization for Chart 1 (Optional)
plt.figure(figsize=(10, 6))
plt.bar(top_pizza_data['pizza_type_id'], top_pizza_data['quantity'], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.title('Top 5 Pizza Types by Quantity Sold')
plt.xlabel('Pizza Type')
plt.ylabel('Quantity Sold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() 
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
            "y": {"beginAtZero": True, "title": {"display": True, "text": "Number of Orders"}},
            "x": {"title": {"display": True, "text": "Hour"}}
        },
        "plugins": {"title": {"display": True, "text": "Orders by Hour of Day"}}
    }
}
print("\nChart 2: Orders by Hour of Day (for Canvas Panel)")
print(chart2)

# Matplotlib Visualization for Chart 2 (Optional)
plt.figure(figsize=(10, 6))
plt.plot(orders_by_hour.index, orders_by_hour.values, marker='o', color='#ff7f0e', label='Orders')
plt.title('Orders by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.legend()
plt.grid(True)
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()  

# Chart 3: Total Sales by Category (Bar Chart)
category_data = sales_by_category.reset_index().head(5)  # Top 5 categories
chart3 = {
    "type": "bar",
    "data": {
        "labels": category_data['category'].tolist(),
        "datasets": [{
            "label": "Total Sales ($)",
            "data": category_data['total_price'].tolist(),
            "backgroundColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
            "borderColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
            "borderWidth": 1
        }]
    },
    "options": {
        "scales": {
            "y": {"beginAtZero": True, "title": {"display": True, "text": "Total Sales ($)"}},
            "x": {"title": {"display": True, "text": "Category"}}
        },
        "plugins": {"title": {"display": True, "text": "Top 5 Categories by Total Sales"}}
    }
}
print("\nChart 3: Top 5 Categories by Total Sales (for Canvas Panel)")
print(chart3)


plt.figure(figsize=(10, 6))
plt.bar(category_data['category'], category_data['total_price'], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.title('Top 5 Categories by Total Sales')
plt.xlabel('Category')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()  

# Chart 4: Orders by Day of Week (Bar Chart)
day_data = orders_by_day.reset_index()
chart4 = {
    "type": "bar",
    "data": {
        "labels": day_data['day_of_week'].tolist(),
        "datasets": [{
            "label": "Number of Orders",
            "data": day_data['order_id'].tolist(),
            "backgroundColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"],
            "borderColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"],
            "borderWidth": 1
        }]
    },
    "options": {
        "scales": {
            "y": {"beginAtZero": True, "title": {"display": True, "text": "Number of Orders"}},
            "x": {"title": {"display": True, "text": "Day of Week"}}
        },
        "plugins": {"title": {"display": True, "text": "Orders by Day of Week"}}
    }
}
print("\nChart 4: Orders by Day of Week (for Canvas Panel)")
print(chart4)

# Matplotlib Visualization for Chart 4 (Optional)
plt.figure(figsize=(10, 6))
plt.bar(day_data['day_of_week'], day_data['order_id'], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'])
plt.title('Orders by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() 

# Step 5: Detailed Findings
print("\nDetailed Findings:")
print(f"1. Total Revenue: ${total_revenue:.2f} across all orders, indicating a strong sales performance as of {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S %z')}.")  # Current date/time
print("2. Top 5 Pizza Types:")
for idx, row in top_pizza_data.iterrows():
    print(f"   - {row['pizza_type_id']}: {row['quantity']} units sold")
print("3. Peak Sales Hours: Highest order volumes occur between {peak_start} and {peak_end} with {peak_orders} orders, suggesting key meal times.")
print("4. Sales by Category: Categories with the highest revenue include {top_categories}, highlighting popular product lines.")
print("5. Weekly Trends: Order distribution across days shows highest on {peak_day} with {peak_day_orders} orders, indicating potential demand patterns.")

# Step 6: Business Recommendations (Dynamic)
print("\nBusiness Recommendations:")
# Dynamically determine peak hours
peak_hour = orders_by_hour.idxmax()
peak_orders = orders_by_hour.max()
peak_hour_range = orders_by_hour[orders_by_hour > peak_orders * 0.8].index.tolist()  # 80% of peak as threshold
print(f"1. Target promotions during peak hours ({min(peak_hour_range)}:{'00' if min(peak_hour_range) < 12 else '00'} - {max(peak_hour_range)}:{'00' if max(peak_hour_range) < 12 else '00'}) to capitalize on high demand.")
# Top pizza types
top_pizza_list = top_pizza_data['pizza_type_id'].head(3).tolist()  # Top 3 for focus
print(f"2. Focus marketing efforts on top-selling pizzas ({', '.join(top_pizza_list)}) to maximize revenue.")
# Top category
top_category = sales_by_category.idxmax()
print(f"3. Analyze underperforming categories (e.g., other than {top_category}) for potential menu adjustments or discounts.")
# Peak day
peak_day = orders_by_day.idxmax()
peak_day_orders = orders_by_day.max()
print(f"4. Optimize staffing and inventory on {peak_day} with {peak_day_orders} orders to handle peak demand.")

plt.show()  