export interface BaseAddress {
  type: 'usa' | 'international';
  street1: string;
  street2?: string;
  city: string;
}

export interface USAAddress extends BaseAddress {
  type: 'usa';
  state: string;
  zipCode: string;
  county?: string;
}

export interface InternationalAddress extends BaseAddress {
  type: 'international';
  region?: string;
  postalCode?: string;
  country: string;
  province?: string;
}

export type Address = USAAddress | InternationalAddress;
