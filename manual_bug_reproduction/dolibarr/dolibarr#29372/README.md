### Dolibarr Bug 29372 Reproduction – Leave (Holiday) Permission

This README documents how to reproduce the Dolibarr **Leave (Holiday) permission bug** reported in [#29372](https://github.com/Dolibarr/dolibarr/issues/29372).

---

### Start Buggy Version

```bash
defects4rest checkout -p dolibarr -b 16 --buggy --start
```

Complete the Dolibarr installer at [http://localhost:8080](http://localhost:8080/) and create your admin username and password.

---

### Setup

1. Enable **Leave (Holiday)** module:
   `Home → Setup → Modules/Applications → HRM → Leave (Holiday) → Enable`
2. Create a **new test user**:

   * Only give permission:

     * Read leave requests (your leave and those of your subordinates)
   * Do **not** enable:

     * Read all leave requests

---

### Reproduce Bug

1. Log in with the **test user**.
2. Access the restricted page directly via URL:

```text
http://<yourdomain>/holiday/month_report.php?mainmenu=hrm&leftmenu=holiday
```

3. Observe:

* **Buggy Behavior:** The Monthly statement page loads and shows leave information even though the user does not have “read all” permission.
![Buggy Response](./img/image.png)

---

### Verify Patched Version

1. Stop buggy version:

```bash
defects4rest checkout -p dolibarr -b 72 --stop
```

2. Start patched version:

```bash
defects4rest checkout -p dolibarr -b 72 --patched --start
```

3. Re-run the same URL as the test user. The page should now block access for unauthorized users.
 ![Patched Response](./img/image_2.png)
