# Privacy Policy

When you use `borb`, you’re trusting us with your information. 
We understand this is a big responsibility and work hard to protect your information and put you in control.

This **Privacy Policy** is meant to help you understand what information we collect, 
why we collect it, and how you can update, manage, export, and delete your information.

## 1. Information we collect as you use our services

When you use `borb`, you are (by default) sending anonymous usage information to one of our servers.
`borb` sends information upon creating and upon reading a PDF (although this may change in future releases). 
These are roughly the steps followed:

1. Upon installing `borb`, a random user ID is generated
2. This user ID is stored in the installation directory of `borb` (assuming the right file-permissions, etc)
3. Whenever a read/write operation is performed, `borb` sends the following data:
   1. **anonymous_user_id** (A randomly generated ID, associated with your user/installation of `borb`)
   2. **event** (The action that triggered sending statistics, this could be `PDF::loads` or `PDF::dumps`)
   3. **number_of_pages** (the number of pages read/written)
   4. **sys_platform** (which operating system you are using `borb` on)
   5. **utc_time_in_ms**
   6. **version** (which version of `borb` you are using)

***Note:** In order to determine your location (city, country_code, country_name, latitude, longitude, state) a free online API is used*

## 2. We use data to build better services

We use this data to ensure our services are top-quality.
For instance, knowing which versions of `borb` are currently in use enables to decide which versions to continue to support.
Similarly, we may also decide to invest extra developer-time in supporting arabic scripts should we see a market in this. 
And then there is the big split of investing effort into the "reading PDF documents" versus "writing PDF documents" code. 
This is yet another example of where having user data helps.

### 2.1 Provide, maintain and improve our services

By being able to measure specific usages of `borb` (e.g. "reading a PDF", "writing a PDF", etc) we are able to determine where to invest
developer-time. This in turn improves your experience with `borb` as we are continually orienting ourselves to the user-demands.

### 2.3 Develop new services

By knowing our customers, we may develop new products and services that are tailored towards a specific market.

### 2.4 Measure performance

By knowing the amount of PDF documents created/read with each version, we can get idea of the popularity and adoption rate of each version of `borb`.
This gives us the opportunity to fine-tune our release-cycle.

### 2.6 Protect `borb`, our users, and the public

We want to ensure developer-effort is spent on those issues that impact the most users. In order to ensure this, we need to know how many people are using
a given version of `borb`.

## 3. You have choices regarding the information we collect and how it's used

You can disable the gathering of anonymous usage statistics, all you need to do is call `UsageStatistics.disable()`.
This in turn will call `AnonymousUserID.disable()` which will replace the file (containing your user ID) with a 0 byte file.
This is the signal to the rest of `borb` not to send the usage statistics anymore.

Should you so desire, you can (re-) enable them by calling `UsageStatistics.enable()`.
