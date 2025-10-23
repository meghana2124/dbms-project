    def delete_record(self):
        """Deletes the currently selected record using its Primary Key."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return

        table_name = self.table_name_var.get()
        
        try:
            # 1. Get Primary Key Info
            from utils import get_table_primary_key
            pk_columns = get_table_primary_key(self.conn, table_name)
            
            if not pk_columns:
                messagebox.showwarning("Error", f"Could not identify Primary Key for {table_name}.")
                return
                
            # 2. Retrieve Data for the selected row
            selected_data = self.tree.item(selected_item, 'values')
            
            # 3. Get column headers to map data index to PK column name
            headers = self.tree["columns"]
            
            # Build the WHERE clause (handles both single and composite keys)
            where_clauses = []
            pk_values = []
            
            for pk_col in pk_columns:
                try:
                    col_index = headers.index(pk_col)
                    pk_value = selected_data[col_index]
                    where_clauses.append(f"{pk_col} = %s")
                    pk_values.append(pk_value)
                except ValueError:
                    messagebox.showerror("Error", f"Primary Key column '{pk_col}' not found in display data.")
                    return

            # 4. Confirmation
            pk_display = ", ".join([f"{c}={v}" for c, v in zip(pk_columns, pk_values)])
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete the following record from {table_name}?\n\nKey: {pk_display}"
            )

            if confirm:
                cursor = self.conn.cursor()
                sql = f"DELETE FROM {table_name} WHERE {' AND '.join(where_clauses)}"
                
                # 5. Execute Delete
                cursor.execute(sql, tuple(pk_values))
                self.conn.commit()
                messagebox.showinfo("Success", "Record deleted successfully.")
                self.read_data() # Refresh table view
                
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to delete record. Check foreign key constraints: {err}")
            self.conn.rollback()
        except Exception as e:
            messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    # --- END of REPLACE delete_record ---