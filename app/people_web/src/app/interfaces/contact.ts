export interface Contact {
  id?: number;
  // it is not the case that everyone has a first and last name
  firstName?: string;
  lastName: string;
  email?: string;
  phone?: string;
  address?: {
    street?: string;
    city?: string;
    state?: string;
    zipCode?: string;
    country?: string;
  };
  company?: string;
  jobTitle?: string;
  notes?: string;
  birthday?: Date;
  profileImage?: string;
  favorite?: boolean;
  tags?: string[];
  createdAt?: Date;
  updatedAt?: Date;
}
