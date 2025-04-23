export interface BaseAddress {
  type: 'usa' | 'international';
  name: string;
  email?: string;
  phone?: string;
}

export interface USAAddress extends BaseAddress {
  type: 'usa';
  street1: string;
  street2?: string;
  city: string;
  state: string;
  zipCode: string;
  county?: string;
}

export interface InternationalAddress extends BaseAddress {
  type: 'international';
  street1: string;
  street2?: string;
  city: string;
  region?: string;
  postalCode?: string;
  country: string;
  province?: string;
}

export type Address = USAAddress | InternationalAddress;
