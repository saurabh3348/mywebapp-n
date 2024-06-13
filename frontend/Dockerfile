# Use a base image
FROM nginx:alpine

# Copy HTML files to the nginx html directory
COPY templates/index.html /usr/share/nginx/html/index.html

# Create an empty favicon.ico file (optional)
RUN touch /usr/share/nginx/html/favicon.ico

# Expose port
EXPOSE 80

# Command to run the frontend
CMD ["nginx", "-g", "daemon off;"]
