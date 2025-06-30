# ![borb logo](https://github.com/jorisschellekens/borb/raw/master/logo/borb_square_64_64.png) Privacy Policy

When you use `borb`, you’re trusting us with your information.  
We understand this is a big responsibility and work hard to protect your data and put you in control.

This **Privacy Policy** is designed to help you understand what information we collect, why we collect it, and how you can manage your preferences.

---

## 1. Information We Collect

By default, when you use `borb`, anonymous usage statistics are sent to a secure endpoint managed by us.  
These events are triggered when you **read** or **write** a PDF document using `borb`.

### 1.1 What is collected

Each time a read/write operation is performed, the following data may be sent:

- **event**: the action performed (e.g., `"read_pdf"`, `"write_pdf"`)
- **number_of_documents**: the number of documents processed
- **number_of_pages**: the number of pages processed
- **version**: the installed version of `borb`
- **operating_system**: the OS/platform used (e.g., `linux`, `win32`, `darwin`)
- **license_valid_from_in_ms / license_valid_until_in_ms**: if a license is present, the validity period (in milliseconds since epoch)
- **company**: if specified in the license metadata

### 1.2 What is **not** collected

- No personally identifiable information (PII) is collected
- No document content, metadata, or filenames are transmitted
- No user IDs or persistent tracking identifiers are involved

### 1.3 When data is sent

- Events are queued in-memory
- Once the queue exceeds a certain threshold or the application exits, data is aggregated and transmitted securely
- If the system is unlicensed and usage crosses a threshold, a friendly reminder is shown (no telemetry is sent as a result of this reminder)

---

## 2. Why We Collect This Data

The purpose of collecting anonymous usage data is to improve the overall quality and focus of `borb`'s development.

### 2.1 Improve Existing Features

Understanding how `borb` is used (e.g., reading vs. writing PDFs, document sizes) helps us prioritize development and optimize performance.

### 2.2 Version Adoption and Support Lifecycle

By tracking version usage, we can make data-driven decisions on which versions to support or deprecate.

### 2.3 License Insights (If Applicable)

If a license is present, we use its metadata to understand enterprise usage patterns—again, anonymously.

### 2.4 Safeguard Developer Resources

Usage statistics help us allocate engineering effort where it has the highest impact—focusing on popular paths, platforms, and use cases.

---

## 3. Your Control Over Data Collection

### 3.1 Disabling Usage Statistics

You can opt out of telemetry collection at any time by calling:

```python
UsageStatistics.opt_out()
```

This prevents any further anonymous events from being sent.

### 3.2 Re-enabling Usage Statistics

If you wish to opt back in, you can do so via:

```python
UsageStatistics.opt_in()
```

### 3.3 Behavior Without a License

If no license is found, `borb` tracks the number of documents processed (locally). Once a predefined threshold is exceeded, it shows a usage reminder, but no data is sent unless you’ve opted in.

## 4. Summary

We strive to ensure transparency and respect for your privacy.
The telemetry system in borb is intentionally lightweight, anonymous, and fully opt-in/opt-out.

For any questions or concerns, reach out to us at: `borbpdf@gmail.com`