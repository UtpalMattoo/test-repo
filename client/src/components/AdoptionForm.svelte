<script lang="ts">
  import { onMount } from 'svelte';
  
  export let dogId: number;
  export let hasApplication: boolean = false;
  
  let applicantName: string = '';
  let applicantEmail: string = '';
  let applicantPhone: string = '';
  let isSubmitting: boolean = false;
  let showSuccess: boolean = false;
  let errors: Record<string, string> = {};
  
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };
  
  const validatePhone = (phone: string): boolean => {
    // Accept various US phone formats: (555) 123-4567, 555-123-4567, 5551234567
    const phoneRegex = /^(\d{10}|(\d{3}[-.]?\d{3}[-.]?\d{4})|(\(\d{3}\)\s?\d{3}[-.]?\d{4}))$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
  };
  
  const validateForm = (): boolean => {
    errors = {};
    
    if (!applicantName.trim()) {
      errors.name = 'Name is required';
    } else if (applicantName.length < 2) {
      errors.name = 'Name must be at least 2 characters';
    } else if (applicantName.length > 50) {
      errors.name = 'Name must be 50 characters or less';
    }
    
    if (!applicantEmail.trim()) {
      errors.email = 'Email is required';
    } else if (!validateEmail(applicantEmail)) {
      errors.email = 'Invalid email format';
    }
    
    if (!applicantPhone.trim()) {
      errors.phone = 'Phone is required';
    } else if (!validatePhone(applicantPhone)) {
      errors.phone = 'Invalid phone number';
    }
    
    return Object.keys(errors).length === 0;
  };
  
  const handleSubmit = async (event: Event): Promise<void> => {
    event.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    isSubmitting = true;
    
    try {
      const response = await fetch(`/api/dogs/${dogId}/applications`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          applicant_name: applicantName,
          applicant_email: applicantEmail,
          applicant_phone: applicantPhone,
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        showSuccess = true;
        // Reset form
        applicantName = '';
        applicantEmail = '';
        applicantPhone = '';
        // Update parent component that application was submitted
        hasApplication = true;
      } else {
        if (data.field) {
          errors[data.field.replace('applicant_', '')] = data.error;
        } else {
          errors.general = data.error || 'Failed to submit application';
        }
      }
    } catch (error) {
      errors.general = 'Network error. Please try again.';
    } finally {
      isSubmitting = false;
    }
  };
</script>

{#if hasApplication}
  <div class="has-application-message" data-testid="has-application-message">
    <p class="text-yellow-400 font-medium">
      🐕 This dog already has an application and is no longer accepting new applications.
    </p>
  </div>
{:else if showSuccess}
  <div class="success-message" data-testid="success-message">
    <p class="text-green-400 font-medium">
      ✅ Application submitted successfully! We'll be in touch soon.
    </p>
  </div>
{:else}
  <form class="adoption-form" data-testid="adoption-form" on:submit={handleSubmit}>
    <h3 class="text-xl font-semibold text-white mb-4">Apply to Adopt</h3>
    
    {#if errors.general}
      <div class="error-message text-red-400 mb-4" data-testid="general-error">
        {errors.general}
      </div>
    {/if}
    
    <div class="form-group mb-4">
      <label for="applicant-name" class="block text-gray-300 mb-2">Full Name</label>
      <input
        id="applicant-name"
        type="text"
        bind:value={applicantName}
        data-testid="applicant-name"
        class="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:border-blue-500"
        placeholder="Enter your full name"
        maxlength="50"
      />
      {#if errors.name}
        <div class="text-red-400 text-sm mt-1" data-testid="name-error">
          {errors.name}
        </div>
      {/if}
    </div>
    
    <div class="form-group mb-4">
      <label for="applicant-email" class="block text-gray-300 mb-2">Email Address</label>
      <input
        id="applicant-email"
        type="email"
        bind:value={applicantEmail}
        data-testid="applicant-email"
        class="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:border-blue-500"
        placeholder="Enter your email address"
        maxlength="320"
      />
      {#if errors.email}
        <div class="text-red-400 text-sm mt-1" data-testid="email-error">
          {errors.email}
        </div>
      {/if}
    </div>
    
    <div class="form-group mb-6">
      <label for="applicant-phone" class="block text-gray-300 mb-2">Phone Number</label>
      <input
        id="applicant-phone"
        type="tel"
        bind:value={applicantPhone}
        data-testid="applicant-phone"
        class="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:border-blue-500"
        placeholder="(555) 123-4567"
        maxlength="15"
      />
      {#if errors.phone}
        <div class="text-red-400 text-sm mt-1" data-testid="phone-error">
          {errors.phone}
        </div>
      {/if}
    </div>
    
    <button
      type="submit"
      disabled={isSubmitting}
      data-testid="submit-application"
      class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200"
    >
      {#if isSubmitting}
        <span data-testid="submit-loading">Submitting...</span>
      {:else}
        Submit Application
      {/if}
    </button>
  </form>
{/if}

<style>
  .adoption-form {
    background-color: #1f2937;
    padding: 1.5rem;
    border-radius: 0.5rem;
    border: 1px solid #374151;
    margin-top: 1rem;
  }
  
  .has-application-message,
  .success-message {
    background-color: #1f2937;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #374151;
    margin-top: 1rem;
    text-align: center;
  }
  
  .form-group input:focus {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
</style>