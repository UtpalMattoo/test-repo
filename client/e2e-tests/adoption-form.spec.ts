import { test, expect } from '@playwright/test';

test.describe('Adoption Form', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to a dog detail page for testing
    await page.goto('/dog/1');
  });

  test('successful application submission', async ({ page }) => {
    // This test should FAIL initially (form doesn't exist yet)
    
    // Check that adoption form is visible for available dogs
    await expect(page.locator('[data-testid="adoption-form"]')).toBeVisible();
    
    // Fill out the form
    await page.fill('[data-testid="applicant-name"]', 'John Doe');
    await page.fill('[data-testid="applicant-email"]', 'john.doe@example.com');
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    
    // Submit the form
    await page.click('[data-testid="submit-application"]');
    
    // Check for success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('submission accepted');
    
    // Form should be hidden after successful submission
    await expect(page.locator('[data-testid="adoption-form"]')).not.toBeVisible();
  });

  test('form validation errors', async ({ page }) => {
    // This test should FAIL initially (form doesn't exist yet)
    
    await expect(page.locator('[data-testid="adoption-form"]')).toBeVisible();
    
    // Try to submit empty form
    await page.click('[data-testid="submit-application"]');
    
    // Check for validation errors
    await expect(page.locator('[data-testid="name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="phone-error"]')).toBeVisible();
    
    // Test invalid email format
    await page.fill('[data-testid="applicant-name"]', 'John Doe');
    await page.fill('[data-testid="applicant-email"]', 'invalid-email');
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    await page.click('[data-testid="submit-application"]');
    
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toContainText('Invalid email format');
    
    // Test invalid phone format
    await page.fill('[data-testid="applicant-email"]', 'john@example.com');
    await page.fill('[data-testid="applicant-phone"]', '123');
    await page.click('[data-testid="submit-application"]');
    
    await expect(page.locator('[data-testid="phone-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="phone-error"]')).toContainText('Invalid phone number');
    
    // Test name too long (over 50 characters)
    const longName = 'A'.repeat(51);
    await page.fill('[data-testid="applicant-name"]', longName);
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    await page.click('[data-testid="submit-application"]');
    
    await expect(page.locator('[data-testid="name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="name-error"]')).toContainText('Name must be 50 characters or less');
  });

  test('dog with existing application', async ({ page }) => {
    // This test should FAIL initially (functionality doesn't exist yet)
    
    // Mock a dog that already has an application
    // This would typically be set up by seeding test data or mocking API responses
    await page.route('**/api/dogs/1', async route => {
      const json = {
        id: 1,
        name: 'Buddy',
        breed: 'Labrador',
        status: 'available',
        has_application: true
      };
      await route.fulfill({ json });
    });
    
    await page.reload();
    
    // Form should not be visible
    await expect(page.locator('[data-testid="adoption-form"]')).not.toBeVisible();
    
    // Should show "already has application" message
    await expect(page.locator('[data-testid="has-application-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="has-application-message"]')).toContainText('already has an application');
  });

  test('staff applications view', async ({ page }) => {
    // This test should FAIL initially (staff view doesn't exist yet)
    
    // Navigate to staff applications page (this route doesn't exist yet)
    await page.goto('/applications');
    
    // Check that applications list is visible
    await expect(page.locator('[data-testid="applications-list"]')).toBeVisible();
    
    // Mock some applications data
    await page.route('**/api/applications', async route => {
      const json = [
        {
          id: 1,
          dog_id: 1,
          applicant_name: 'John Doe',
          applicant_email: 'john@example.com',
          applicant_phone: '(555) 123-4567',
          submission_timestamp: '2025-10-09T10:00:00',
          application_status: 'PENDING'
        },
        {
          id: 2,
          dog_id: 2,
          applicant_name: 'Jane Smith',
          applicant_email: 'jane@example.com',
          applicant_phone: '555-123-4567',
          submission_timestamp: '2025-10-09T11:00:00',
          application_status: 'PENDING'
        }
      ];
      await route.fulfill({ json });
    });
    
    await page.reload();
    
    // Check that applications are displayed
    await expect(page.locator('[data-testid="application-item"]')).toHaveCount(2);
    await expect(page.locator('[data-testid="application-item"]').first()).toContainText('John Doe');
    await expect(page.locator('[data-testid="application-item"]').nth(1)).toContainText('Jane Smith');
  });

  test('form loading states', async ({ page }) => {
    // This test should FAIL initially (loading states don't exist yet)
    
    await expect(page.locator('[data-testid="adoption-form"]')).toBeVisible();
    
    // Fill out form
    await page.fill('[data-testid="applicant-name"]', 'John Doe');
    await page.fill('[data-testid="applicant-email"]', 'john.doe@example.com');
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    
    // Mock slow network response to test loading state
    await page.route('**/api/dogs/1/applications', async route => {
      // Delay response to test loading state
      await new Promise(resolve => setTimeout(resolve, 1000));
      const json = { message: 'submission accepted', application_id: 42 };
      await route.fulfill({ json, status: 201 });
    });
    
    // Submit form and check loading state
    await page.click('[data-testid="submit-application"]');
    
    // Should show loading state
    await expect(page.locator('[data-testid="submit-loading"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-application"]')).toBeDisabled();
    
    // Wait for submission to complete
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-loading"]')).not.toBeVisible();
  });

  test('network error handling', async ({ page }) => {
    // This test should FAIL initially (error handling doesn't exist yet)
    
    await expect(page.locator('[data-testid="adoption-form"]')).toBeVisible();
    
    // Fill out form
    await page.fill('[data-testid="applicant-name"]', 'John Doe');
    await page.fill('[data-testid="applicant-email"]', 'john.doe@example.com');
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    
    // Mock network failure
    await page.route('**/api/dogs/1/applications', async route => {
      await route.abort('failed');
    });
    
    // Submit form
    await page.click('[data-testid="submit-application"]');
    
    // Check for network error message
    await expect(page.locator('[data-testid="general-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="general-error"]')).toContainText('Network error');
  });

  test('long input field validation', async ({ page }) => {
    // This test should FAIL initially (validation doesn't exist yet)
    
    await expect(page.locator('[data-testid="adoption-form"]')).toBeVisible();
    
    // Test extremely long email (over 320 chars)
    const longEmail = 'a'.repeat(300) + '@example.com';
    await page.fill('[data-testid="applicant-name"]', 'John Doe');
    await page.fill('[data-testid="applicant-email"]', longEmail);
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    
    await page.click('[data-testid="submit-application"]');
    
    // Should show email error
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    
    // Test very long phone number
    await page.fill('[data-testid="applicant-email"]', 'john@example.com');
    await page.fill('[data-testid="applicant-phone"]', '555-123-4567-extension-12345');
    
    await page.click('[data-testid="submit-application"]');
    
    // Should show phone error
    await expect(page.locator('[data-testid="phone-error"]')).toBeVisible();
  });

  test('server error response handling', async ({ page }) => {
    // This test should FAIL initially (error handling doesn't exist yet)
    
    await expect(page.locator('[data-testid="adoption-form"]')).toBeVisible();
    
    // Fill out form
    await page.fill('[data-testid="applicant-name"]', 'John Doe');
    await page.fill('[data-testid="applicant-email"]', 'john.doe@example.com');
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    
    // Mock server error
    await page.route('**/api/dogs/1/applications', async route => {
      const json = { error: 'Internal server error' };
      await route.fulfill({ json, status: 500 });
    });
    
    // Submit form
    await page.click('[data-testid="submit-application"]');
    
    // Check for server error message
    await expect(page.locator('[data-testid="general-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="general-error"]')).toContainText('Internal server error');
  });

  test('form validation edge cases', async ({ page }) => {
    // This test should FAIL initially (edge case validation doesn't exist yet)
    
    await expect(page.locator('[data-testid="adoption-form"]')).toBeVisible();
    
    // Test whitespace-only name
    await page.fill('[data-testid="applicant-name"]', '   ');
    await page.fill('[data-testid="applicant-email"]', 'john@example.com');
    await page.fill('[data-testid="applicant-phone"]', '(555) 123-4567');
    
    await page.click('[data-testid="submit-application"]');
    
    // Should show name error
    await expect(page.locator('[data-testid="name-error"]')).toBeVisible();
    
    // Test email with just spaces
    await page.fill('[data-testid="applicant-name"]', 'John Doe');
    await page.fill('[data-testid="applicant-email"]', '   ');
    
    await page.click('[data-testid="submit-application"]');
    
    // Should show email error
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
  });
});